#!/usr/bin/env python3
"""Build the kid's read-only Library. Kiosk (as root): sudo python3 library/build_library.py
The desktop app calls build() to get the books and pictures.
Safe to run again: it skips files that exist and resumes cut downloads.
Env: LIB_ROOT=<dir> (default /var/lib/art-kit/Library; ~/Library links to it)  CACHE=<dir> (default /var/cache/art-kit)
     DRY=1 (print actions only)  ONLY=<regex> (use only list lines that match, for tests)
     BLENDER_SRC=<dir> (Blender manual source, default /tmp/books/blender-manual)
Needs: Python 3, pypdfium2 (page images and text), Pillow.
"""
import glob, os, re, runpy, shutil, ssl, sys, threading, urllib.request, zipfile
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
TOTAL_MB = 3700  # the work: about 1.5 GB to download + 2.2 GB of page images (measured 2026-11). About 3 GB stays on disk.
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
PDFIUM = threading.Lock()  # PDFium is not thread-safe (the desktop app also makes PDF thumbnails)
try:  # the desktop app bundles certifi: a clean Mac or another Linux has no CA files where the build Python looks
    import certifi
    urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPSHandler(
        context=ssl.create_default_context(cafile=certifi.where()))))
except ImportError:
    pass  # the kiosk: the system CA store


def rows(path, only='.'):
    """The data lines of a list file that match ONLY, split by '|'."""
    with open(path, encoding='utf-8') as f:
        return [l.rstrip('\n').split('|') for l in f
                if not l.startswith('#') and l.strip() and re.search(only, l)]


def col(r, i):
    return r[i] if i < len(r) else ''


def get(url, dst, dry=False, tick=None):
    """Download once into dst. Resume a cut download from dst.part. True if dst is there."""
    if os.path.isfile(dst) and os.path.getsize(dst):
        return True
    if dry:
        print('+ get %s -> %s' % (url, dst))
        return True
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    part, err = dst + '.part', None
    for _ in range(3):
        have = os.path.getsize(part) if os.path.exists(part) else 0
        req = urllib.request.Request(url, headers={'User-Agent': UA, **({'Range': 'bytes=%d-' % have} if have else {})})
        try:
            with urllib.request.urlopen(req, timeout=60) as r, open(part, 'ab' if r.status == 206 else 'wb') as f:
                n = have if r.status == 206 else 0
                cr = r.headers.get('Content-Range', '')
                if r.status == 206 and not cr.startswith('bytes %d-' % have):
                    raise OSError('bad range: %s' % cr)
                size = cr.rpartition('/')[2] if r.status == 206 else r.headers.get('Content-Length', '')
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
                    n += len(b)
                    if tick:
                        tick(n)
            if size.isdigit() and n != int(size):
                raise OSError('cut download: %d of %s bytes' % (n, size))  # the next try goes on from the .part file
            os.replace(part, dst)
            return True
        except HTTPError as e:
            if e.code == 416 and have and e.headers.get('Content-Range') == 'bytes */%d' % have:  # the .part file is complete
                os.replace(part, dst)
                return True
            err = e
            if e.code == 416 and have:  # a bad .part file: start again
                os.remove(part)
                continue
            if e.code < 500:
                break
        except OSError as e:
            err = e
    print('download failed: %s (%s)' % (url, err))
    return False


class Links(HTMLParser):
    """The page requisites (wget -p): images, style sheets, icons, scripts. (link, is a style sheet)"""
    def __init__(self):
        super().__init__()
        self.found, self.style = [], False

    def css(self, text):  # url() in style="" and <style>
        self.found += [(r.strip(), False) for r in re.findall(r'url\(\s*[\'"]?([^\'")]+)', text) if not r.startswith('data:')]

    def handle_data(self, data):
        if self.style:
            self.css(data)

    def handle_endtag(self, tag):
        self.style = self.style and tag != 'style'

    def handle_starttag(self, tag, attrs):
        a, rel = dict(attrs), set((dict(attrs).get('rel') or '').lower().split())
        self.style = tag == 'style'
        self.css(a.get('style') or '')
        if tag in ('img', 'script', 'input', 'source') and a.get('src'):
            self.found.append((a['src'], False))
        if tag in ('img', 'source') and a.get('srcset'):
            self.found += [(x.split()[0], False) for x in a['srcset'].split(',') if x.strip()]
        if tag == 'link' and a.get('href') and rel & {'stylesheet', 'icon'}:
            self.found.append((a['href'], 'stylesheet' in rel))


def safe(name):
    """A file name from a URL: no folders, no '..', no characters that Windows does not allow."""
    name = re.sub(r'[\x00-\x1f/\\]' + (r'|[<>:"|?*]' if os.name == 'nt' else ''), '_', name)
    return '_' + name if name.startswith('.') else name


def local_name(url, used, css=False):
    """wget -nd -E names: the last path part (+ ?query), .css for style sheets, .1 .2 for a second file of the same name."""
    u = urlsplit(url)
    name = os.path.basename(u.path) or 'index.html'
    if u.query:
        name += ('@' if os.name == 'nt' else '?') + u.query  # wget: '@' on Windows
    name = safe(name)
    if css and not name.endswith('.css'):
        name += '.css'
    base, i = name, 0
    while name in used:
        i += 1
        name = '%s.%d' % (base, i)
    used.add(name)
    return name


def html_page(d, files, full, used):
    """wget -E: a file that is an HTML page (an error page for a missing image) gets .html."""
    p = os.path.join(d, files[full])
    if os.path.isfile(p) and not p.endswith('.html'):
        with open(p, 'rb') as f:
            if f.read(512).lstrip().lower().startswith((b'<!doctype html', b'<html')):
                files[full] += '.html'
                used.add(files[full])
                os.replace(p, p + '.html')


def save(url, d, dry=False):
    """An offline copy of one web page and its images (like wget -p -k -E -nd). Same host only. .done marks a full copy."""
    if os.path.exists(os.path.join(d, '.done')):
        return True
    if dry:
        print('+ save %s -> %s' % (url, d))
        return True
    orig = url  # wget names the file after the URL in the list, not after a redirect
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
            url, page = r.geturl(), r.read().decode(r.headers.get_content_charset() or 'utf-8', 'replace')
    except OSError as e:
        print('download failed: %s (%s)' % (url, e))
        return False
    os.makedirs(d, exist_ok=True)
    if os.path.islink(d) or any(os.path.islink(x) for x in glob.glob(os.path.join(glob.escape(d), '*'))):  # writes stay in d
        print('skip %s: a link in %s' % (url, d))
        return False
    host, used, ok, files, p = urlsplit(url).netloc, set(), True, {}, Links()
    u = urlsplit(orig)  # wget -E: the page file name ends in .html ('/' gives index.html)
    name = safe((os.path.basename(u.path) or 'index.html') + (('@' if os.name == 'nt' else '?') + u.query if u.query else ''))
    name += '' if re.search(r'\.html?$', name, re.I) else '.html'
    used.add(name)
    p.feed(page)
    for ref, css in dict.fromkeys(p.found):
        full = urljoin(url, ref).split('#')[0]
        if urlsplit(full).netloc != host or full in files:
            continue  # same host only (no fonts or video players)
        files[full] = local_name(full, used, css)
        ok = get(full, os.path.join(d, files[full])) and ok
        html_page(d, files, full, used)
    for full, f in list(files.items()):  # images in the style sheets
        if f.endswith('.css') and os.path.exists(os.path.join(d, f)):
            text = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
            for ref in dict.fromkeys(re.findall(r'url\(\s*[\'"]?([^\'")]+)', text)):
                img = urljoin(full, ref)
                if urlsplit(img).netloc == host and not ref.startswith('data:'):
                    if img not in files:
                        files[img] = local_name(img, used)
                        ok = get(img, os.path.join(d, files[img])) and ok
                        html_page(d, files, img, used)
                    text = text.replace(ref, files[img])
            with open(os.path.join(d, f), 'w', encoding='utf-8') as fh:
                fh.write(text)

    def link(m):  # -k: saved files get the local name, all other links the full URL
        full = urljoin(url, m.group(2)).split('#')[0]
        return m.group(1) + (files[full].replace('?', '%3F') if full in files else urljoin(url, m.group(2))) + m.group(3)
    page = re.sub(r'''(\s(?:src|href)=["'])([^"'#][^"']*)(["'])''', link, page)
    with open(os.path.join(d, name), 'w', encoding='utf-8') as fh:
        fh.write(page)
    if ok:
        open(os.path.join(d, '.done'), 'w', encoding='utf-8').close()
    return ok


def render(pdf, out, pages, remove, tick=None):
    """Books/<name>/page-NNN.png (120 dpi) + page-NNN.txt (NNN = PDF page number). tick(page, pages, bytes of the page images)."""
    import pypdfium2
    with PDFIUM:
        doc, size = pypdfium2.PdfDocument(pdf), 0
        n = len(doc)
    first, last = (1, n) if pages == 'all' else map(int, pages.split('-'))
    for p in range(first, min(last, n) + 1):
        if str(p) in remove:
            continue
        png, txt = os.path.join(out, 'page-%03d.png' % p), os.path.join(out, 'page-%03d.txt' % p)
        if not (os.path.isfile(png) and os.path.getsize(png)) or not os.path.exists(txt):
            with PDFIUM:  # one page at a time: the thumbnails can go in between
                page = doc[p - 1]
                if not (os.path.isfile(png) and os.path.getsize(png)):
                    page.render(scale=120 / 72).to_pil().save(png + '.tmp', 'PNG')
                    os.replace(png + '.tmp', png)
                if not os.path.exists(txt):
                    tp = page.get_textpage()
                    with open(txt + '.tmp', 'w', encoding='utf-8') as f:
                        f.write(tp.get_text_range().replace('\r\n', '\n'))
                    os.replace(txt + '.tmp', txt)
                    tp.close()
                page.close()
        size += os.path.getsize(png)
        if tick:
            tick(p - first + 1, last - first + 1, size)
    with PDFIUM:
        doc.close()
    for p in remove:  # removed pages never stay
        for f in glob.glob(os.path.join(out, 'page-%03d.*' % int(p))):
            os.remove(f)


def unzip(z, d, dry=False):
    """Unpack into d.part, then rename it to d: d is there only when all of the archive is. False: a bad archive (it is removed)."""
    if dry:
        print('+ unzip %s -> %s' % (z, d))
        return True
    shutil.rmtree(d + '.part', ignore_errors=True)
    try:
        with zipfile.ZipFile(z) as f:
            f.extractall(d + '.part')
    except (OSError, zipfile.BadZipFile) as e:
        print('bad archive %s (%s): it downloads again at the next run' % (z, e))
        os.remove(z)
        return False
    shutil.rmtree(d, ignore_errors=True)
    os.replace(d + '.part', d)
    return True


def lessons(lib, kit=KIT, dry=False):
    """Tutorials/<Topic>/<lesson>/ = the lesson folders (no RULES/COURSE/REVIEW/INDEX files)."""
    for topic in sorted(glob.glob(os.path.join(kit, 'lessons', '*', ''))):
        t = os.path.basename(topic.rstrip(os.sep))
        for lesson in sorted(glob.glob(os.path.join(topic, '*', ''))):
            dst = os.path.join(lib, 'Tutorials', t, os.path.basename(lesson.rstrip(os.sep)))
            if dry:
                print('+ copy %s -> %s' % (lesson, dst))
            else:
                shutil.copytree(lesson, dst, dirs_exist_ok=True)
    for r, _, fs in os.walk(os.path.join(lib, 'Tutorials')):
        for f in fs:
            if f in ('RULES.md', 'COURSE.md', 'REVIEW.md', 'INDEX.md') and not dry:
                os.remove(os.path.join(r, f))


def index(lib, kit=KIT):
    """Search index. make-index.py takes the home dir that holds Library/."""
    if os.path.basename(lib) != 'Library':
        return print('skip index: make-index.py needs a folder named Library')
    argv, sys.argv = sys.argv, ['make-index.py', '--root', os.path.dirname(lib)]
    try:
        runpy.run_path(os.path.join(kit, 'app', 'make-index.py'), run_name='__main__')
    finally:
        sys.argv = argv


def credits(lib, here=HERE):
    """CREDITS.md from all lists."""
    L = lambda f: rows(os.path.join(here, f)) if os.path.exists(os.path.join(here, f)) else []
    out = ['# Credits', '', '## Books (Books/<name>/)'] + ['- %s: %s <%s>' % (col(r, 1), col(r, 5), col(r, 2)) for r in L('books.txt')]
    out += ['', '## Manuals',
            '- Krita-Manual: Krita Manual, the Krita team, GNU FDL 1.3 <https://docs.krita.org/en/epub/KritaManual.epub>',
            "- SweetHome3D-Guide: Sweet Home 3D User's Guide, Space Mushrooms <https://www.sweethome3d.com/users-guide/>.",
            '  The site footer says: "© Copyright 2026 Space Mushrooms - All rights reserved" (no open license for the guide text).',
            '- Blender-Manual/Grease-Pencil: Blender Manual, Blender Documentation Team, CC BY-SA 4.0 <https://docs.blender.org/manual/>',
            '', '## Painting'] + ['- Pepper-and-Carrot/%s: %s' % (col(r, 0), col(r, 2)) for r in L('revoy.txt')]
    out += ['- Brushes: David Revoy, Krita brushes 2025-01 bundle, CC0 <https://www.davidrevoy.com/article1060/krita-brushes-2025-01-bundle>']
    if L('revoy-pages.txt'):
        out += ['', '## Revoy'] + ['- %s: David Revoy, %s, %s <%s>' % (col(r, 0), col(r, 2), col(r, 3), col(r, 1)) for r in L('revoy-pages.txt')]
    out += ['', '## Inspiration (Art Institute of Chicago open access, CC0)'] + ['- %s/%s: %s' % (col(r, 0), col(r, 1), col(r, 3)) for r in L('inspiration.txt')]
    out += ['', '## Tutorials', '- Art Kit lessons. Each lesson names its sources in its README.md.']
    with open(os.path.join(lib, 'CREDITS.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')


def modes(lib):
    """Root-owned (as root), read-only for all. "From Family" belongs to 60-backup.sh."""
    for r, ds, fs in os.walk(lib):
        if r == lib and 'From Family' in ds:
            ds.remove('From Family')
        for p in [r] + [os.path.join(r, f) for f in fs]:
            if os.path.islink(p):
                continue
            if os.geteuid() == 0:
                os.chown(p, 0, 0)
            m = os.stat(p).st_mode
            os.chmod(p, (m | 0o444 | (0o111 if os.path.isdir(p) or m & 0o111 else 0)) & ~0o022 & 0o7777)


def build(lib, cache, kit=KIT, dry=False, only='.', blender_src='/tmp/books/blender-manual', check=False, progress=None):
    """Download and make the Library. progress(done, total, text, mb) after each step and each MB. Returns the TODO list (empty = all done)."""
    here, todo = os.path.join(kit, 'library'), []
    L = lambda f: rows(os.path.join(here, f), only) if os.path.exists(os.path.join(here, f)) else []
    books, insp, eps, pages = L('books.txt'), L('inspiration.txt'), L('revoy.txt'), L('revoy-pages.txt')
    total, state = len(books) + len(insp) + len(eps) + len(pages) + 6, {'done': 0, 'bytes': 0, 'now': 0}

    def step(text, part=0.0):  # part: how far the current step is (0..1)
        if progress:
            progress(state['done'] + part, total, text, (state['bytes'] + state['now']) >> 20)

    def done():
        state['done'] += 1
        step('')

    def fetch(url, dst, text=''):  # get(), and count the MB (also of files that are there from an earlier run)
        ok = get(url, dst, dry, lambda n: state.update(now=n) or step('%s (%d MB)' % (text, n >> 20) if text else ''))
        state['now'] = 0
        state['bytes'] += os.path.getsize(dst) if ok and not dry else 0
        return ok
    if not dry:
        os.makedirs(lib, exist_ok=True)
        os.makedirs(cache, exist_ok=True)

    # 0. Check every book URL (HTTP 200 after redirects).
    if check:
        print('== URL check (books.txt)')
        for r in books:
            try:
                with urllib.request.urlopen(urllib.request.Request(col(r, 2), method='HEAD', headers={'User-Agent': UA}), timeout=30) as x:
                    code = x.status
            except HTTPError as e:
                code = e.code
            except OSError:
                code = '000'
            print(code, col(r, 1))

    # 1. Books/<name>/page-NNN.png + page-NNN.txt (NNN = PDF page number).
    for i, r in enumerate(books):
        name, url, pg, remove = col(r, 1), col(r, 2), col(r, 3), col(r, 4).split()
        text = 'Book %d of %d: %s' % (i + 1, len(books), name.replace('-', ' '))
        pdf, out = os.path.join(cache, name + '.pdf'), os.path.join(lib, 'Books', name)
        step(text)
        if not fetch(url, pdf, text):
            print('skip %s (download failed)' % name)
            todo.append('book ' + name)
        elif dry:
            print('+ render %s pages=%s remove=[%s]' % (name, pg, ' '.join(remove)))
        else:
            os.makedirs(out, exist_ok=True)
            try:
                render(pdf, out, pg, remove, lambda a, b, n: state.update(now=n) or step('%s (page %d of %d)' % (text, a, b), a / b))
            except Exception as e:  # a bad PDF in the cache: remove it, go on with the next book
                print('skip %s (bad PDF: %s); it downloads again at the next run' % (name, e))
                os.remove(pdf)
                todo.append('book ' + name)
            state['bytes'] += state['now']
            state['now'] = 0
        done()

    # 2. Manuals.
    step('Krita Manual')
    if fetch('https://docs.krita.org/en/epub/KritaManual.epub', os.path.join(cache, 'KritaManual.epub'), 'Krita Manual'):
        if not os.path.exists(os.path.join(lib, 'Krita-Manual', 'index.xhtml')) and \
                not unzip(os.path.join(cache, 'KritaManual.epub'), os.path.join(lib, 'Krita-Manual'), dry):
            todo.append('Krita Manual')
    else:
        todo.append('Krita Manual')
    done()
    step('Sweet Home 3D Guide')
    if not save('https://www.sweethome3d.com/users-guide/', os.path.join(lib, 'SweetHome3D-Guide'), dry):
        todo.append('Sweet Home 3D Guide')
    done()
    if os.path.isdir(os.path.join(blender_src, 'manual', 'grease_pencil')):
        if dry:
            print('+ copy Blender manual')
        else:
            shutil.copytree(os.path.join(blender_src, 'manual', 'grease_pencil'), os.path.join(lib, 'Blender-Manual', 'Grease-Pencil'), dirs_exist_ok=True)
            shutil.copy(os.path.join(blender_src, 'LICENSE'), os.path.join(lib, 'Blender-Manual', 'LICENSE.txt'))
    else:
        print('TODO: Blender Manual (Grease Pencil) not found in %s' % blender_src)
        todo.append('Blender Manual')
    done()

    # 3. Inspiration/<collection>/<file> + Inspiration/CREDITS.txt
    for i, r in enumerate(insp):
        step('Picture %d of %d' % (i + 1, len(insp)))
        if not fetch(col(r, 2), os.path.join(lib, 'Inspiration', col(r, 0), col(r, 1))):
            print('skip %s' % col(r, 1))
            todo.append('picture ' + col(r, 1))
        done()
    if not dry:
        os.makedirs(os.path.join(lib, 'Inspiration'), exist_ok=True)
        # Same columns as inspiration.txt (folder|file|url|credit): make-index.py reads this file.
        with open(os.path.join(lib, 'Inspiration', 'CREDITS.txt'), 'w', encoding='utf-8') as f:
            f.writelines('|'.join(r) + '\n' for r in insp)

    # 4. Painting: Pepper&Carrot .kra sources (David Revoy, CC BY 4.0) and his brush bundle (CC0).
    pc = os.path.join(lib, 'Painting', 'Pepper-and-Carrot')
    for i, r in enumerate(eps):
        ep, text = col(r, 0), 'Pepper&Carrot %d of %d' % (i + 1, len(eps))
        if fetch(col(r, 1), os.path.join(cache, ep + '.zip'), text):
            if not glob.glob(os.path.join(pc, ep, '*.kra')) and not unzip(os.path.join(cache, ep + '.zip'), os.path.join(pc, ep), dry):
                todo.append(ep)
        else:
            print('skip %s' % ep)
            todo.append(ep)
        done()
    br, brd = 'https://www.peppercarrot.com/extras/resources/deevad-bundle_25.01.zip', os.path.join(lib, 'Painting', 'Brushes')  # from davidrevoy.com/article1060
    if fetch(br, os.path.join(cache, 'deevad-bundle_25.01.zip'), 'Brushes'):
        if not (os.path.isdir(brd) and os.listdir(brd)) and not unzip(os.path.join(cache, 'deevad-bundle_25.01.zip'), brd, dry):
            todo.append('Brushes')
    else:
        todo.append('Brushes')
    done()

    # 5. Revoy/<slug>/: offline copies of the pages in revoy-pages.txt (slug|url|title|license).
    for r in pages:
        step('David Revoy: %s' % col(r, 2))
        if not save(col(r, 1), os.path.join(lib, 'Revoy', col(r, 0)), dry):
            todo.append('Revoy ' + col(r, 0))
        done()

    # 6. Tutorials, 7. CREDITS.md, 8. search index, 9. owner and modes.
    step('Lessons and search')
    lessons(lib, kit, dry)
    if not dry:
        credits(lib, here)
        index(lib, kit)
        if os.name == 'posix':
            modes(lib)
    done()
    return todo


def main():
    lib = os.environ.get('LIB_ROOT', '/var/lib/art-kit/Library')
    todo = build(lib, os.environ.get('CACHE', '/var/cache/art-kit'), dry=bool(os.environ.get('DRY')),
                 only=os.environ.get('ONLY', '.'), blender_src=os.environ.get('BLENDER_SRC', '/tmp/books/blender-manual'),
                 check=not os.environ.get('DRY'))
    if not os.environ.get('DRY'):
        print('== Sizes')
        for d in sorted(os.listdir(lib)) + ['']:
            p = os.path.join(lib, d)
            n = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs) if os.path.isdir(p) else os.path.getsize(p)
            print('%6d MB  %s' % (n >> 20, p))
    if todo:
        print('TODO: ' + ' '.join(todo))


if __name__ == '__main__':
    main()
