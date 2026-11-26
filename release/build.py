#!/usr/bin/env python3
"""Build the Art Kit desktop bundle on this computer (Linux x64, Windows x64, or macOS arm64/x64).
  python3 release/build.py fetch     get the pinned apps (apps.toml) into release/cache and check each SHA-256
  python3 release/build.py app       build the Art Kit app with PyInstaller (build/pyi/)
  python3 release/build.py pack      pack the bundle into dist/ (Linux tar.gz, Windows installer, macOS DMG) + SHA256SUMS
  python3 release/build.py sources   get the apps' source archives into dist/sources (GPL)
Needs: pip install -r release/requirements.txt. Windows: Inno Setup 6. Downloads resume.
"""
import glob, hashlib, os, platform, shutil, subprocess, sys, tarfile, tomllib, zipfile

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'library'))
from build_library import get

VERSION = open(os.path.join(R, 'app', 'VERSION')).read().strip()
CACHE, BUILD, DIST = os.path.join(R, 'release', 'cache'), os.path.join(R, 'build'), os.path.join(R, 'dist')
ARCH = 'arm64' if platform.machine().lower() in ('arm64', 'aarch64') else 'x64'
PLAT = {'linux': 'linux-x64', 'win32': 'windows-x64', 'darwin': 'macos-' + ARCH}[sys.platform]
APPS = tomllib.load(open(os.path.join(R, 'release', 'apps.toml'), 'rb'))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fetch(section=PLAT, into=CACHE):
    """Download each file of a section once, then check its SHA-256. A wrong file stops the build."""
    out = {}
    for name, a in APPS[section].items():
        p = os.path.join(into, a['url'].rsplit('/', 1)[1])
        if not get(a['url'], p):
            sys.exit('download failed: ' + a['url'])
        if sha256(p) != a['sha256']:
            os.remove(p)
            sys.exit('SHA-256 does not match: %s (the file is removed)' % a['url'])
        print('ok  %s  %s' % (a['sha256'], os.path.basename(p)))
        out[name] = p
    return out


def top(src, dst):
    """Move the one top folder of an unpacked archive to dst."""
    (d,) = [p for p in glob.glob(os.path.join(src, '*')) if os.path.isdir(p)]
    shutil.move(d, dst)
    shutil.rmtree(src)


def run(*argv):
    print('+ ' + ' '.join(argv))
    subprocess.run(argv, check=True)


def app():
    run(sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--distpath', os.path.join(BUILD, 'pyi'),
        '--workpath', os.path.join(BUILD, 'work'), os.path.join(R, 'release', 'art-kit.spec'))


def linux(f):
    """ArtKit-x.y.z-x86_64.tar.gz: ArtKit.AppImage, Krita.AppImage, Blender/, SweetHome3D/, install.sh."""
    name = 'ArtKit-%s-x86_64' % VERSION
    s, ad = os.path.join(BUILD, name), os.path.join(BUILD, 'AppDir')
    shutil.copytree(os.path.join(BUILD, 'pyi', 'artkit'), ad, symlinks=True)
    os.symlink('artkit', os.path.join(ad, 'AppRun'))
    shutil.copy(os.path.join(R, 'release', 'icon.png'), os.path.join(ad, 'art-kit.png'))
    with open(os.path.join(ad, 'art-kit.desktop'), 'w') as d:
        d.write('[Desktop Entry]\nType=Application\nName=Art Kit\nExec=artkit\nIcon=art-kit\nCategories=Education;Graphics;\n')
    os.makedirs(s)
    os.chmod(f['appimagetool'], 0o755)
    subprocess.run([f['appimagetool'], '--appimage-extract-and-run', '--no-appstream', '--runtime-file', f['appimage-runtime'],
                    ad, os.path.join(s, 'ArtKit.AppImage')],
                   check=True, env=dict(os.environ, ARCH='x86_64'))
    shutil.copy(f['krita'], os.path.join(s, 'Krita.AppImage'))
    os.chmod(os.path.join(s, 'Krita.AppImage'), 0o755)
    for key, dst in (('blender', 'Blender'), ('sweethome3d', 'SweetHome3D')):
        with tarfile.open(f[key]) as t:
            t.extractall(os.path.join(BUILD, key), filter='tar')
        top(os.path.join(BUILD, key), os.path.join(s, dst))
    for x in ('install.sh', 'icon.png'):
        shutil.copy(os.path.join(R, 'release', x), s)
    with tarfile.open(os.path.join(DIST, name + '.tar.gz'), 'w:gz', compresslevel=6) as t:
        t.add(s, name)


def windows(f):
    """ArtKit-Setup-x.y.z.exe (Inno Setup): Art Kit, Krita, Blender, Sweet Home 3D in Program Files\\Art Kit."""
    s = os.path.join(BUILD, 'stage')
    shutil.copytree(os.path.join(BUILD, 'pyi', 'Art Kit'), s)
    for key, dst in (('krita', 'Krita'), ('blender', 'Blender')):
        with zipfile.ZipFile(f[key]) as z:
            z.extractall(os.path.join(BUILD, key))
        top(os.path.join(BUILD, key), os.path.join(s, dst))
    # The Sweet Home 3D installer holds 32- and 64-bit files: let it pick the right ones, then take its folder.
    run(f['sweethome3d'], '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/NOICONS', '/DIR=' + os.path.join(s, 'Sweet Home 3D'))
    for u in glob.glob(os.path.join(s, 'Sweet Home 3D', 'unins*')):
        os.remove(u)
    wv2 = os.path.join(BUILD, 'MicrosoftEdgeWebview2Setup.exe')  # Microsoft's small WebView2 bootstrapper (signed; it changes: no pin)
    if not get('https://go.microsoft.com/fwlink/p/?LinkId=2124703', wv2):
        sys.exit('download failed: WebView2 bootstrapper')
    iscc = shutil.which('iscc') or r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
    run(iscc, '/DVersion=' + VERSION, '/DStage=' + s, '/DWebView2=' + wv2, '/O' + DIST,
        os.path.join(R, 'release', 'art-kit.iss'))


def mac(f):
    """ArtKit-x.y.z-<arch>.dmg: an "Art Kit" folder (Art Kit.app + the three upstream apps, unchanged) and an Applications link."""
    root = os.path.join(BUILD, 'dmg')
    s = os.path.join(root, 'Art Kit')
    os.makedirs(s)
    run('ditto', os.path.join(BUILD, 'pyi', 'Art Kit.app'), os.path.join(s, 'Art Kit.app'))
    for key in ('krita', 'blender', 'sweethome3d'):
        mnt = os.path.join(BUILD, 'mnt-' + key)
        subprocess.run(['hdiutil', 'attach', '-nobrowse', '-readonly', '-noautoopen', '-mountpoint', mnt, f[key]],
                       input=b'Y\n' * 50, check=True, stdout=subprocess.DEVNULL)  # "Y": a license page, if any
        (a,) = [p for p in glob.glob(os.path.join(mnt, '*.app')) if not os.path.islink(p)]
        run('ditto', a, os.path.join(s, os.path.basename(a)))
        run('hdiutil', 'detach', mnt)
    os.symlink('/Applications', os.path.join(root, 'Applications'))
    run('hdiutil', 'create', '-volname', 'Art Kit', '-srcfolder', root, '-ov', '-format', 'UDZO',
        os.path.join(DIST, 'ArtKit-%s-%s.dmg' % (VERSION, ARCH)))


def pack():
    f = fetch()
    for d in glob.glob(os.path.join(BUILD, '*')):
        if os.path.basename(d) not in ('pyi', 'work'):
            shutil.rmtree(d) if os.path.isdir(d) and not os.path.islink(d) else os.remove(d)
    os.makedirs(DIST, exist_ok=True)
    {'linux': linux, 'win32': windows, 'darwin': mac}[sys.platform](f)
    sums()


def sums():
    files = sorted(p for p in glob.glob(os.path.join(DIST, '*')) if os.path.isfile(p) and not p.endswith('SHA256SUMS'))
    with open(os.path.join(DIST, 'SHA256SUMS'), 'w') as out:
        for p in files:
            out.write('%s  %s\n' % (sha256(p), os.path.basename(p)))
            print('%6d MB  %s' % (os.path.getsize(p) >> 20, os.path.basename(p)))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'fetch':
        fetch()
    elif cmd == 'app':
        app()
    elif cmd == 'pack':
        pack()
    elif cmd == 'sources':
        fetch('source', os.path.join(DIST, 'sources'))
    else:
        sys.exit(__doc__)
