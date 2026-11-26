"""Library app backend. No GTK here, so it can be tested alone.

handle(uri) -> (status, mime, bytes). Paths come from the root dir:
  ROOT/Library (read-only), ROOT/Art (kid's files), ROOT/.cache/library.
"""
import datetime, html, json, os, random, re, shutil, sqlite3, subprocess
from urllib.parse import urlsplit, parse_qs, unquote, quote

APP = os.path.dirname(os.path.abspath(__file__))
IMG = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
MIME = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
        '.svg': 'image/svg+xml', '.txt': 'text/plain; charset=utf-8'}
LESSON = re.compile(r'^(\d{3}) (.+)$')
# Shelf names a kid understands. The folder names do not change.
LABELS = {'Revoy': "David Revoy's Studio"}
try:
    from PIL import Image  # python3-pillow: small thumbnails save memory on 2 GB
except ImportError:
    Image = None


def plain(md):
    """Markdown -> plain text for search snippets."""
    md = re.sub(r'(^|\n)\s*(#+|[-*]|\d+\.)\s+', ' ', md)
    return re.sub(r'\s+', ' ', re.sub(r'\*\*|__|`|^#+|\[|\]\([^)]*\)', '', md))


def short_name(path):
    """'Alphonse-Mucha_Zodiaque-La-Plume_111986.jpg' -> 'zodiaque-la-plume.jpg'"""
    stem, ext = os.path.splitext(os.path.basename(path))
    parts = stem.split('_')
    stem = parts[1] if len(parts) == 3 else stem
    if re.match(r'page-\d+$', stem):  # a book page: add the book name
        stem = '-'.join(os.path.basename(os.path.dirname(path)).split('-')[:2]) + '-' + stem
    words = re.findall(r'[a-z0-9]+', stem.lower())
    return '-'.join(words[:4] if len(words) > 4 else words)[:40] + ext.lower()


def parse_read(line):
    """'**Read:** A, PDF pages 3–4; B, section X' -> [(source, [3, 4]), ('B, section X', [])]"""
    out = []
    for seg in line.split('**Read:**', 1)[-1].split(';'):
        seg = seg.strip()
        m = re.match(r'^(.*?),?\s*PDF pages?\s+(.*)$', seg)
        if not m:
            if seg:
                out.append((seg, []))
            continue
        pages = []
        for a, b in re.findall(r'(\d+)(?:\s*[–-]\s*(\d+))?', re.sub(r'\([^)]*\)', '', m.group(2))):
            pages += range(int(a), int(b or a) + 1)
        out.append((m.group(1).strip(), pages))
    return out


class Library:
    def __init__(self, root, launch=None):
        self.lib = os.path.join(root, 'Library')
        self.art = os.path.join(root, 'Art')
        self.cache = os.path.join(root, '.cache', 'library')
        self.launch = launch or (lambda argv: subprocess.Popen(argv))
        with open(os.path.join(APP, 'books-map.json')) as f:
            self.books = json.load(f)
        self.deck = []

    # ---------- helpers ----------
    def url(self, path):
        """library:// URL for a file under Library or the cache."""
        for base, host in ((self.lib, 'lib'), (self.cache, 'cache'), (self.art, 'art')):
            if path.startswith(base + os.sep):
                return 'library://%s/%s' % (host, quote(os.path.relpath(path, base)))
        raise ValueError(path)

    def inside(self, rel, base=None):
        base = base or self.lib
        p = os.path.realpath(os.path.join(base, rel))
        if not p.startswith(os.path.realpath(base) + os.sep):
            raise ValueError('outside library')
        return p

    def done(self):
        try:
            with open(os.path.join(self.art, '.library-log')) as f:
                return {l.rstrip('\n').split('\t', 1)[1] for l in f if '\t' in l}
        except FileNotFoundError:
            return set()

    def credits(self):
        c = {}
        try:
            with open(os.path.join(self.lib, 'Inspiration', 'CREDITS.txt')) as f:
                for l in f:
                    p = l.rstrip('\n').split('|')
                    if len(p) == 4 and not l.startswith('#'):
                        c[(p[0], p[1])] = p[3].replace(', CC0', '').replace(' / ', ' · ')
        except FileNotFoundError:
            pass
        return c

    def images(self, coll):
        d = os.path.join(self.lib, 'Inspiration', coll)
        return sorted(f for f in os.listdir(d) if f.lower().endswith(IMG))

    def image(self, coll, f, credits=None):
        credits = self.credits() if credits is None else credits
        p = os.path.join(self.lib, 'Inspiration', coll, f)
        return {'coll': coll, 'file': f, 'url': self.url(p), 'rel': os.path.relpath(p, self.lib), 'thumb': self.thumb_url(p),
                'credit': credits.get((coll, f), '')}

    def thumb_url(self, p):
        return self.url(p).replace('library://lib/', 'library://thumb/', 1)

    def thumb(self, rel):
        """A 400 px JPEG in ~/.cache/library/thumbs, made on first use. No Pillow: the original."""
        src = self.inside(rel)
        if Image is None:
            return src
        t = os.path.join(self.cache, 'thumbs', re.sub(r'\W', '_', rel) + '.jpg')
        if not os.path.exists(t) or os.path.getmtime(t) < os.path.getmtime(src):
            os.makedirs(os.path.dirname(t), exist_ok=True)
            with Image.open(src) as im:
                im.draft('RGB', (400, 400))  # JPEG: decode small, uses less memory
                im = im.convert('RGB')
                im.thumbnail((400, 400))
                im.save(t + '.tmp', 'JPEG', quality=82)
            os.replace(t + '.tmp', t)
        return t

    # ---------- tutorials ----------
    def topics(self):
        t, done = os.path.join(self.lib, 'Tutorials'), self.done()
        out = []
        order = ['Drawing', 'Painting', 'Revoy', 'Design', 'Lettering', 'Interior Design', '3D Drawing']
        key = lambda n: (order.index(n) if n in order else len(order), n)
        for name in sorted(os.listdir(t), key=key) if os.path.isdir(t) else []:
            ls = self.lessons(name, done)
            if ls:
                out.append({'name': name, 'label': LABELS.get(name, name), 'count': len(ls), 'done': sum(l['done'] for l in ls)})
        return out

    def lessons(self, topic, done=None):
        done = self.done() if done is None else done
        d = os.path.join(self.lib, 'Tutorials', topic)
        out = []
        for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            m = LESSON.match(name)
            if m and os.path.isfile(os.path.join(d, name, 'README.md')):
                out.append({'dir': name, 'num': m.group(1), 'title': m.group(2),
                            'done': '%s/%s' % (topic, name) in done})
        return out

    def page(self, book, n):
        p = os.path.join(self.lib, 'Books', book, 'page-%03d.png' % n)
        return {'book': book, 'page': n, 'url': self.url(p) if os.path.exists(p) else '',
                'rel': os.path.relpath(p, self.lib)}

    def lesson(self, topic, dir):
        import markdown
        text = open(os.path.join(self.inside(os.path.join('Tutorials', topic, dir)), 'README.md')).read()
        pages, other, head, body = [], [], {}, []
        text, _, source = text.partition('\n---\nSource:')
        for line in text.splitlines():
            m = re.match(r'\*\*(You make|Builds on|Time|Read):\*\*\s*(.*?)\s*$', line)
            if m:
                head[m.group(1)] = m.group(2)
            else:  # drop "(Norton, PDF 20)": the Source line names the book
                body.append(re.sub(r'\s*\([^()]*\bPDF (pages? )?\d[^()]*\)', '', line))
            if line.startswith('**Read:**'):
                for src, nums in parse_read(line):
                    if not nums:
                        other.append(src)
                    elif src in self.books:
                        pages += [dict(self.page(self.books[src], n), source=src) for n in nums]
                    else:
                        other.append(src + ' (book not found)')
        ls = self.lessons(topic)
        i = [l['dir'] for l in ls].index(dir)
        nums = re.findall(r'\d{3}', head.get('Builds on', ''))  # the last one is the one just before
        first = next(({'dir': l['dir'], 'title': l['title']} for l in ls if nums and l['num'] == max(nums)), None)
        make = re.sub(r'~/Art/([^/]+)/([^/\s]+\.\w+)', r'<b>\2</b> in your \1 folder', html.escape(head.get('You make', '')))
        html_ = re.sub(r'(You should see:)', r'<span class="see">\1</span>', markdown.markdown('\n'.join(body)))
        return {'topic': topic, 'label': LABELS.get(topic, topic), 'dir': dir, 'title': ls[i]['title'], 'num': ls[i]['num'],
                'done': ls[i]['done'], 'html': html_, 'pages': pages, 'other': other,
                'make': make, 'time': head.get('Time', ''), 'first': first,
                'source': '; '.join(x for x in (head.get('Read', ''), source.strip()) if x),
                'prev': ls[i - 1]['dir'] if i > 0 else '', 'next': ls[i + 1]['dir'] if i + 1 < len(ls) else ''}

    def mark_done(self, topic, dir):
        os.makedirs(self.art, exist_ok=True)
        with open(os.path.join(self.art, '.library-log'), 'a') as f:
            f.write('%s\t%s/%s\n' % (datetime.datetime.now().isoformat(timespec='seconds'), topic, dir))
        return {'ok': True}

    def book_page(self, book, n):
        r = self.page(book, n)
        r['prev'] = n - 1 if self.page(book, n - 1)['url'] else 0
        r['next'] = n + 1 if self.page(book, n + 1)['url'] else 0
        return r

    # ---------- inspire ----------
    def collections(self):
        d = os.path.join(self.lib, 'Inspiration')
        return [{'name': c, 'count': len(self.images(c)),
                 'cover': next((self.thumb_url(os.path.join(d, c, f)) for f in self.images(c)), '')} for c in sorted(os.listdir(d))
                if os.path.isdir(os.path.join(d, c))] if os.path.isdir(d) else []

    def lucky(self):
        if not self.deck:  # no repeats until all are seen
            self.deck = [(c['name'], f) for c in self.collections() for f in self.images(c['name'])]
            random.shuffle(self.deck)
        if not self.deck:
            return {}
        return self.image(*self.deck.pop())

    def save(self, rel):
        src = self.inside(rel)
        dst = os.path.join(self.art, 'Favorites')
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, os.path.join(dst, os.path.basename(src)))
        return {'ok': True}

    def picks(self):
        d = os.path.join(self.art, 'Favorites')
        return [{'url': self.url(os.path.join(d, f)), 'name': f, 'rel': f, 'art': 1}
                for f in sorted(os.listdir(d)) if f.lower().endswith(IMG)] if os.path.isdir(d) else []

    def krita(self, rel, art=False):
        """Copy the picture to ~/Art/Inspire with a short name, so she can save it. Then open the copy."""
        src = self.inside(rel, os.path.join(self.art, 'Favorites') if art else None)
        dst = os.path.join(self.art, 'Inspire', short_name(src))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):  # keep her changes if she opened it before
            shutil.copyfile(src, dst)
            os.chmod(dst, 0o644)
        self.launch(['krita', dst])
        return {'ok': True, 'name': os.path.basename(dst)}

    # ---------- family + note ----------
    def family(self):
        d = os.path.join(self.lib, 'From Family')
        out = []
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            p, ext = os.path.join(d, f), os.path.splitext(f)[1].lower()
            if ext in IMG:
                out.append({'name': f, 'kind': 'image', 'url': self.url(p), 'thumb': self.thumb_url(p), 'rel': os.path.relpath(p, self.lib)})
            elif ext == '.txt':
                out.append({'name': f, 'kind': 'text', 'text': open(p, errors='replace').read()})
            elif ext == '.pdf':
                os.makedirs(self.cache, exist_ok=True)
                png = os.path.join(self.cache, 'family-%s.png' % re.sub(r'\W', '_', f))
                if not os.path.exists(png) or os.path.getmtime(png) < os.path.getmtime(p):
                    subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '100', '-png', '-singlefile',
                                    p, png[:-4]], check=False)
                if os.path.exists(png):
                    out.append({'name': f, 'kind': 'image', 'url': self.url(png)})
        return out

    def note(self, text):
        d = os.path.join(self.art, 'Notes')
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, datetime.datetime.now().strftime('%Y-%m-%d-%H%M') + '.txt')
        with open(p, 'a') as f:
            f.write(text.rstrip() + '\n')
        return {'ok': True, 'file': os.path.basename(p)}

    def notes(self):
        """Her notes, newest first."""
        d = os.path.join(self.art, 'Notes')
        out = []
        for f in sorted(os.listdir(d), reverse=True) if os.path.isdir(d) else []:
            if f.endswith('.txt'):
                try:
                    when = datetime.datetime.strptime(f[:15], '%Y-%m-%d-%H%M').strftime('%a %d %b %Y, %H:%M')
                except ValueError:
                    when = f[:-4]
                out.append({'when': when, 'file': f, 'text': open(os.path.join(d, f), errors='replace').read()})
        return out

    def delete_note(self, f):
        """Move the note to Notes/Deleted (the backup keeps it, a parent can bring it back)."""
        d = os.path.join(self.art, 'Notes')
        p = self.inside(f, d)
        os.makedirs(os.path.join(d, 'Deleted'), exist_ok=True)
        os.replace(p, os.path.join(d, 'Deleted', os.path.basename(p)))
        return {'ok': True}

    # ---------- search ----------
    def search(self, q):
        words = re.findall(r'\w+', q)
        db = os.path.join(self.lib, 'index.sqlite')
        if not words or not os.path.exists(db):
            return {'lessons': [], 'pages': [], 'images': []}
        fts = ' '.join('"%s"*' % w for w in words)
        con = sqlite3.connect('file:%s?mode=ro' % quote(db), uri=True)
        out = {'lessons': [], 'pages': [], 'images': []}
        credits = self.credits()
        whole = [re.compile(r'\b%s\b' % re.escape(w), re.I) for w in words]
        rows = con.execute("SELECT kind, title, ref, snippet(docs, 3, char(1), char(2), '…', 14), body FROM docs "
                           "WHERE docs MATCH ? ORDER BY rank LIMIT 200", (fts,)).fetchall()
        # Title with the whole word first, then the whole word in the text, then "cat" in "catch".
        rows.sort(key=lambda x: 0 if all(w.search(x[1]) for w in whole) else 1 if all(w.search(x[4]) for w in whole) else 2)
        for kind, title, ref, snip, _ in rows:
            snip = html.escape(plain(snip)).replace('\x01', '<b>').replace('\x02', '</b>')
            a, b = ref.split('/', 1)
            r = {'title': title, 'snippet': snip}
            if kind == 'lesson':
                r.update(topic=a, dir=b, title=LABELS.get(a, a) + ' · ' + b)
            elif kind == 'page':
                r.update(book=a, page=int(b))
            else:
                r.update(self.image(a, b, credits))
            if len(out[kind + 's']) < 30:
                out[kind + 's'].append(r)
        con.close()
        return out

    # ---------- dispatcher ----------
    def handle(self, uri):
        u = urlsplit(uri)
        host, path = u.netloc.lower(), unquote(u.path).lstrip('/')
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if host == 'ui':
                p = self.inside(path or 'index.html', os.path.join(APP, 'ui'))
            elif host == 'lib':
                p = self.inside(path)
            elif host == 'cache':
                p = self.inside(path, self.cache)
            elif host == 'thumb':
                p = self.thumb(path)
            elif host == 'art':  # her own pictures (My picks)
                p = self.inside(path, self.art)
            elif host == 'api':
                f = {'topics': lambda: self.topics(),
                     'lessons': lambda: self.lessons(q['topic']),
                     'lesson': lambda: self.lesson(q['topic'], q['dir']),
                     'done': lambda: self.mark_done(q['topic'], q['dir']),
                     'page': lambda: self.book_page(q['book'], int(q['page'])),
                     'collections': lambda: self.collections(),
                     'collection': lambda: [self.image(q['name'], f) for f in self.images(q['name'])],
                     'lucky': lambda: self.lucky(),
                     'save': lambda: self.save(q['rel']),
                     'krita': lambda: self.krita(q['rel'], q.get('art')),
                     'picks': lambda: self.picks(),
                     'delnote': lambda: self.delete_note(q['file']),
                     'family': lambda: self.family(),
                     'note': lambda: self.note(q['text']),
                     'notes': lambda: self.notes(),
                     'search': lambda: self.search(q.get('q', ''))}[path]
                return 200, 'application/json', json.dumps(f()).encode()
            else:
                raise ValueError('bad host')
            with open(p, 'rb') as fh:
                return 200, MIME.get(os.path.splitext(p)[1].lower(), 'application/octet-stream'), fh.read()
        except Exception as e:  # show the error in the UI, never crash the app
            return 404, 'application/json', json.dumps({'error': str(e)}).encode()
