#!/usr/bin/env python3
"""Art Kit desktop app (Windows, Mac, Linux): the Library app in a pywebview window, and the kit apps.
The UI (ui/) and the backend (library.py) are the kiosk's. This file adds a local web server for the UI
(127.0.0.1, random port, a random token on every request), the app row (Krita, Sweet Home 3D, Blender),
first-run app settings, the books download, and a daily update check.
The books and pictures download by themselves at each start until they are all there (one builder: build_library.py).
Data: ~/Art Kit/ (Art/ with Notes/, Library/). Usage: desktop.py [--root DIR] [--selftest | --get-library]
Env: ART_KIT_APPS=<dir> (the bundled apps; default: next to the app)  ART_KIT_UPDATE_URL=<url> (tests)  ART_KIT_KIOSK=1 (no update check)
"""
import argparse, glob, hmac, http.server, json, os, plistlib, re, secrets, shutil, subprocess, sys, tempfile, threading, time
import urllib.request, webbrowser
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlsplit

APP = os.path.dirname(os.path.abspath(__file__))
KIT = getattr(sys, '_MEIPASS', os.path.dirname(APP))  # holds lessons/, library/, app/make-index.py
sys.path[:0] = [APP, os.path.join(KIT, 'library')]
import build_library, library
from library import Library
library.PDFIUM = build_library.PDFIUM  # one PDFium lock: the book download and the thumbnails

VERSION = open(os.path.join(APP, 'VERSION'), encoding='utf-8').read().strip()
RELEASES = 'https://github.com/acetousk/art-kit/releases/'
UPDATE_URL = os.environ.get('ART_KIT_UPDATE_URL', 'https://api.github.com/repos/acetousk/art-kit/releases/latest')
CSP = ("default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "form-action 'none'; frame-src 'none'; object-src 'none'")
MAC, WIN = sys.platform == 'darwin', os.name == 'nt'
# The bundled apps: Linux file (install.sh unpacks the AppImages), Windows file, macOS app name. release/ packs them so.
APPS = {'Krita': ('Krita/AppRun', 'Krita/bin/krita.exe', 'krita'),
        'Sweet Home 3D': ('SweetHome3D/SweetHome3D', 'Sweet Home 3D/SweetHome3D.exe', 'sweet home 3d'),
        'Blender': ('Blender/blender', 'Blender/blender-launcher.exe', 'blender')}  # Windows: the launcher has no console window
# Kit settings, the same as the kiosk (kiosk/install.sh).
KRITARC = 'imageWidthDef=1920\nimageHeightDef=1200\nimageResolutionDef=150\nundoStackLimit=30\nAutoSaveInterval=300\n'
JAVA = '-Xmx700m -XX:+UseSerialGC -Dsun.java2d.opengl=false'
BLENDER = ("import bpy, os\n"  # only when there are no preferences yet: an earlier Blender keeps its own
           "if not os.path.exists(os.path.join(bpy.utils.resource_path('USER'), 'config', 'userpref.blend')):\n"
           "    p = bpy.context.preferences; p.view.show_splash = False; p.inputs.use_mouse_emulate_3_button = True\n"
           "    bpy.ops.wm.save_userpref()\n")


def apps_dir():
    if os.environ.get('ART_KIT_APPS'):
        return os.environ['ART_KIT_APPS']
    if os.environ.get('APPIMAGE'):  # Linux: ArtKit.AppImage sits next to the apps
        return os.path.dirname(os.environ['APPIMAGE'])
    exe = os.path.dirname(os.path.abspath(sys.executable))
    if MAC and '/AppTranslocation/' in exe:  # macOS runs a new download from a random place: look in Applications
        return next((d for d in ('/Applications/Art Kit', os.path.expanduser('~/Applications/Art Kit')) if os.path.isdir(d)), exe)
    return os.path.abspath(os.path.join(exe, '..', '..', '..')) if MAC else exe  # Mac: the "Art Kit" folder with the .app


def find(name):
    """The program file of a bundled app, or None."""
    lin, win, mac = APPS[name]
    if not MAC:
        p = os.path.join(apps_dir(), win if WIN else lin)
        return p if os.path.isfile(p) else None
    for a in glob.glob(os.path.join(apps_dir(), '*.app')):
        if os.path.basename(a).lower().startswith(mac):
            with open(os.path.join(a, 'Contents', 'Info.plist'), 'rb') as f:
                return os.path.join(a, 'Contents', 'MacOS', plistlib.load(f)['CFBundleExecutable'])
    return None


def clean_env():
    """The environment for other programs: without the paths of this app's own bundle (PyInstaller, AppImage, Qt)."""
    own = ('QT_PLUGIN_PATH', 'QML2_IMPORT_PATH', 'QT_STYLE_OVERRIDE', 'QTWEBENGINE_DISABLE_SANDBOX', 'QTWEBENGINE_CHROMIUM_FLAGS',
           'APPDIR', 'APPIMAGE', 'ARGV0', 'OWD')
    env = {k: v for k, v in os.environ.items() if k not in own and not k.startswith('_PYI')}
    if 'LD_LIBRARY_PATH_ORIG' in env:
        env['LD_LIBRARY_PATH'] = env.pop('LD_LIBRARY_PATH_ORIG')
    elif getattr(sys, 'frozen', False):
        env.pop('LD_LIBRARY_PATH', None)
    return env


class Desktop:
    def __init__(self, root):
        self.root, self.lib = root, Library(root, self.launch)
        self.conf_file = os.path.join(root, '.art-kit.json')
        try:
            with open(self.conf_file, encoding='utf-8') as f:
                self.conf = json.load(f)
        except (OSError, ValueError):
            self.conf = {}
        self.job = {'running': False, 'done': 0, 'total': 1, 'text': '', 'mb': 0, 'failed': []}
        self.first = not self.conf.get('library_started')  # the first start shows the download screen
        self.lock = threading.Lock()  # one request at a time in library.py, as in the kiosk app
        self.conf_lock = threading.Lock()
        self.checker = None

    def save_conf(self, **kw):
        with self.conf_lock:  # the download, the update check, and requests all save
            self.conf.update(kw)
            with open(self.conf_file + '.tmp', 'w', encoding='utf-8') as f:
                json.dump(self.conf, f)
            os.replace(self.conf_file + '.tmp', self.conf_file)

    # ---------- first run ----------
    def setup(self):
        """The lessons (they ship in the app) and the search index, once per version."""
        lib = os.path.join(self.root, 'Library')
        os.makedirs(os.path.join(self.root, 'Art'), exist_ok=True)
        if self.conf.get('lessons') != VERSION:
            build_library.lessons(lib, KIT)
            build_library.index(lib, KIT)
            self.save_conf(lessons=VERSION)

    def kit_settings(self):
        home = os.path.expanduser('~')
        rc = (os.path.join(os.environ.get('LOCALAPPDATA', home), 'kritarc') if WIN else
              os.path.join(home, 'Library', 'Preferences', 'kritarc') if MAC else
              os.path.join(os.environ.get('XDG_CONFIG_HOME') or os.path.join(home, '.config'), 'kritarc'))
        if not os.path.exists(rc):
            os.makedirs(os.path.dirname(rc), exist_ok=True)
            with open(rc, 'x', encoding='utf-8') as f:
                f.write(KRITARC)

    # ---------- apps ----------
    def start(self, name, *args, wait=False):
        exe = find(name)
        if not exe:
            raise ValueError('%s is not in this Art Kit' % name)
        env = clean_env()
        if name == 'Sweet Home 3D':
            env['_JAVA_OPTIONS'] = JAVA
        if WIN and getattr(sys, 'frozen', False):  # PyInstaller: the apps must not load this app's DLLs
            import ctypes
            ctypes.windll.kernel32.SetDllDirectoryW(None)

        def run():
            if name == 'Blender' and not self.conf.get('blender'):  # no splash, Emulate 3 Button Mouse (for a pen)
                b = os.path.join(os.path.dirname(exe), 'blender.exe') if WIN else exe
                subprocess.run([b, '-b', '--factory-startup', '--python-expr', BLENDER], env=env, cwd=self.root,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
                               creationflags=0x08000000 if WIN else 0)  # CREATE_NO_WINDOW
                self.save_conf(blender=True)
            subprocess.Popen([exe, *args], env=env, cwd=self.root)
        run() if wait else threading.Thread(target=run, daemon=True).start()
        return {'ok': True}

    def launch(self, argv):
        """library.py: "Open in Krita" -> the bundled Krita."""
        if argv[0] == 'krita':
            return self.start('Krita', *argv[1:])
        subprocess.Popen(argv, env=clean_env())

    # ---------- books and pictures ----------
    def get_library(self, show=None):
        """Download the books and pictures in the background. show(job): run here and report each step (the terminal)."""
        if self.job['running'] or self.conf.get('library'):
            return {'ok': True}
        self.job.update(running=True, failed=[], text='Starting…')
        self.save_conf(library_started=True)
        lib, cache = os.path.join(self.root, 'Library'), os.path.join(self.root, '.cache', 'downloads')

        def progress(d, t, x, mb):
            self.job.update(done=d, total=t, text=x or self.job['text'], mb=mb)
            if show:
                show(self.job)

        def run():
            try:
                todo = build_library.build(lib, cache, KIT, progress=progress)
            except Exception as e:
                todo = [str(e)]
            todo = [t for t in todo if t != 'Blender Manual']  # it comes from a local copy (kiosk admin), not a download
            if not todo:
                shutil.rmtree(cache, ignore_errors=True)  # the PDFs and zips: about 1 GB
                self.save_conf(library=True)
            self.job.update(running=False, failed=todo)
        run() if show else threading.Thread(target=run, daemon=True).start()
        return {'ok': True}

    # ---------- update check ----------
    def check(self):
        """Once a day, ask GitHub for the latest release. Quiet on any error."""
        if os.environ.get('ART_KIT_KIOSK') == '1' or not self.conf.get('updates', True):
            return
        if time.time() - self.conf.get('checked', 0) < 86400 and 'ART_KIT_UPDATE_URL' not in os.environ:
            return
        self.save_conf(checked=time.time())  # also offline: one try a day
        try:
            req = urllib.request.Request(UPDATE_URL, headers={'User-Agent': 'art-kit/' + VERSION, 'Accept': 'application/vnd.github+json'})
            with urllib.request.urlopen(req, timeout=3) as r:
                v = str(json.load(r)['tag_name']).lstrip('v')
            if re.fullmatch(r'\d+\.\d+\.\d+', v):  # the link is the release page of that tag, never a URL from the reply
                self.save_conf(latest={'version': v, 'url': RELEASES + 'tag/v' + v})
        except Exception:
            pass

    def update(self):
        u = self.conf.get('latest')
        num = lambda v: tuple(int(x) for x in v.split('.') if x.isdigit())
        if os.environ.get('ART_KIT_KIOSK') == '1' or not self.conf.get('updates', True) or not u:
            return None
        return u if num(u['version']) > num(VERSION) and u['url'].startswith(RELEASES) else None

    def browse(self, url):
        """A web page in the system browser (never in the Art Kit window)."""
        if not re.match(r'https?://', url):
            return {'ok': False}
        if WIN or MAC:
            webbrowser.open(url)
        else:
            subprocess.Popen(['xdg-open', url], env=clean_env())
        return {'ok': True}

    def open_update(self):
        u = self.update()
        return self.browse(u['url']) if u else {'ok': False}

    # ---------- the desktop API (the kiosk app does not have it) ----------
    def info(self):
        if self.checker:
            self.checker.join(3.5)  # the first home screen waits for the check (3 s at most)
        return {'version': VERSION, 'update': self.update(), 'updates': self.conf.get('updates', True),
                'apps': {n: bool(find(n)) for n in APPS},
                'library': dict(self.job, complete=bool(self.conf.get('library')), first=self.first, total_mb=build_library.TOTAL_MB)}

    def api(self, name, q):
        return {'desktop': self.info,
                'app': lambda: self.start(q['name']),
                'getlib': self.get_library,
                'updates': lambda: self.save_conf(updates=q.get('on') == '1') or {'ok': True},
                'open': self.open_update,
                'link': lambda: self.browse(q.get('url', ''))}[name]()


def serve(desk):
    """The local server: 127.0.0.1 only, a random port, and a random token in a cookie (the first URL has it)."""
    token = secrets.token_urlsafe(32)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlsplit(self.path)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            c = SimpleCookie(self.headers.get('Cookie', ''))
            new = hmac.compare_digest(q.get('t', ''), token)
            if self.headers.get('Host') != '127.0.0.1:%d' % port or not (new or hmac.compare_digest(c['t'].value if 't' in c else '', token)):
                return self.reply(403, 'text/plain', b'no')  # also blocks DNS rebinding (a wrong Host)
            host, _, rest = u.path.lstrip('/').partition('/')
            try:
                if host == 'api' and rest in ('desktop', 'app', 'getlib', 'updates', 'open', 'link'):
                    status, mime, body = 200, 'application/json', json.dumps(desk.api(rest, q)).encode()
                else:
                    with desk.lock:
                        status, mime, body = desk.lib.handle('library://%s/%s%s' % (host, rest, '?' + u.query if u.query else ''))
            except Exception as e:
                status, mime, body = 404, 'application/json', json.dumps({'error': str(e)}).encode()
            if mime == 'application/json':  # library:// links -> this server
                body = body.replace(b'library://', b'/')
            self.reply(status, mime, body, 't=%s; Path=/; HttpOnly; SameSite=Strict' % token if new else None,
                       CSP if host in ('ui', 'api') else CSP + '; sandbox')  # downloaded pages and scripts never run as the UI

        def reply(self, status, mime, body, cookie=None, csp=CSP):
            self.send_response(status)
            for k, v in (('Content-Type', mime), ('Content-Length', str(len(body))), ('Content-Security-Policy', csp),
                         ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'), ('Set-Cookie', cookie)):
                if v:
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    srv.daemon_threads = True
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return 'http://127.0.0.1:%d/ui/index.html?t=%s' % (port, token)


def selftest(url):
    """Headless: the UI, a lesson, and a search through the HTTP API. No window."""
    base = url.split('/ui/')[0]
    get = lambda path, cookie: urllib.request.urlopen(urllib.request.Request(base + path, headers={'Cookie': cookie}), timeout=10)
    with urllib.request.urlopen(url, timeout=10) as r:
        cookie = r.headers['Set-Cookie'].split(';')[0]
        assert b'app.js' in r.read()
    try:
        get('/api/topics', '')
        raise AssertionError('a request without the token worked')
    except urllib.error.HTTPError as e:
        assert e.code == 403
    topics = json.load(get('/api/topics', cookie))
    t = topics[0]['name']
    ls = json.load(get('/api/lessons?topic=' + urllib.parse.quote(t), cookie))
    lesson = json.load(get('/api/lesson?topic=%s&dir=%s' % (urllib.parse.quote(t), urllib.parse.quote(ls[0]['dir'])), cookie))
    assert lesson['html'] and 'error' not in lesson, lesson
    hits = json.load(get('/api/search?q=color', cookie))
    assert hits['lessons'], hits
    info = json.load(get('/api/desktop', cookie))
    import importlib  # the web view code is in the build (it needs no screen to load)
    importlib.import_module('webview.platforms.' + {'darwin': 'cocoa', 'win32': 'winforms'}.get(sys.platform, 'qt' if getattr(sys, 'frozen', False) else 'gtk'))
    print('selftest ok: Art Kit %s, %d topics, lesson "%s", %d search hits, apps %s'
          % (info['version'], len(topics), lesson['title'], len(hits['lessons']), info['apps']))


def terminal(desk):
    """--get-library: the download with a progress line. Ctrl+C stops it; the app goes on at its next start."""
    show = lambda j: print('\r%3d%%  %5d MB of about %.1f GB  %-60.60s' % (min(99, 100 * j['mb'] / build_library.TOTAL_MB), j['mb'],
                                                                         build_library.TOTAL_MB / 1000, j['text']), end='', flush=True)
    print('Getting the books and pictures into %s. Ctrl+C is safe: Art Kit goes on at its next start.' % desk.root)
    try:
        desk.get_library(show)
    except KeyboardInterrupt:
        sys.exit('\nStopped. Art Kit goes on with the download at its next start.')
    print('\nDone. All books and pictures are here.' if desk.conf.get('library') else
          '\nSome files did not download: %s. Art Kit tries again at its next start.' % ', '.join(desk.job['failed']))


def single(root):
    """One Art Kit per data folder (a lock file). None: another Art Kit has it."""
    f = open(os.path.join(root, '.art-kit.lock'), 'a', encoding='utf-8')
    try:
        if WIN:
            import msvcrt
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.close()
        return None
    return f  # keep it open: the lock goes when the app quits


def window(*args, **kw):
    import webview
    webview.create_window('Art Kit', *args, **kw)
    linux_app = getattr(sys, 'frozen', False) and sys.platform.startswith('linux')
    try:  # Qt web view: keep its sandbox. Ubuntu 23.10+ blocks it (AppArmor, user namespaces) for apps without a profile.
        blocked = open('/proc/sys/kernel/apparmor_restrict_unprivileged_userns', encoding='utf-8').read().strip() == '1'
    except OSError:
        blocked = False
    if linux_app and blocked:
        print('Qt sandbox off: this system blocks unprivileged user namespaces (AppArmor). The view shows only Art Kit pages.', file=sys.stderr)
        os.environ.setdefault('QTWEBENGINE_DISABLE_SANDBOX', '1')
    webview.start(gui='qt' if linux_app else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', help='data folder (default: ~/Art Kit)')
    ap.add_argument('--selftest', action='store_true', help='test the API without a window, then quit')
    ap.add_argument('--get-library', action='store_true', help='download the books and pictures here, with progress (Ctrl+C is safe)')
    ap.add_argument('--open', metavar='APP', choices=list(APPS), help='start a bundled app with the kit settings (Start menu)')
    ap.add_argument('--version', action='version', version=VERSION)
    a = ap.parse_args()
    root = os.path.abspath(a.root or (tempfile.mkdtemp() if a.selftest else os.path.join(os.path.expanduser('~'), 'Art Kit')))
    os.makedirs(root, 0o700, exist_ok=True)
    os.chmod(root, 0o700)  # Notes and Art: this user only (also an older folder)
    desk = Desktop(root)
    if a.open:
        return desk.start(a.open, wait=True)
    lock = single(root)
    if not lock:
        if a.selftest or a.get_library:
            sys.exit('Art Kit is open already (%s).' % root)
        return window(html='<p style="font:20px sans-serif;margin:40px">Art Kit is open already.</p>', width=420, height=160)
    desk.setup()
    url = serve(desk)
    if a.selftest:
        try:
            selftest(url)
        except Exception as e:  # an exit code for CI (a windowed app has no console)
            print('selftest FAILED: %r' % e, file=sys.stderr)
            sys.exit(1)
        finally:
            a.root or shutil.rmtree(root, ignore_errors=True)
        return
    if a.get_library:
        return terminal(desk)
    desk.kit_settings()  # Krita defaults, only if there is no Krita config
    desk.get_library()  # starts or goes on with the download (nothing to do when it is done)
    desk.checker = threading.Thread(target=desk.check, daemon=True)
    desk.checker.start()
    window(url, width=1280, height=860, min_size=(800, 600))


if __name__ == '__main__':
    main()
