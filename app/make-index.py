#!/usr/bin/env python3
"""Build the search index ~/Library/index.sqlite (SQLite FTS5).
Run as admin after each library update:  sudo python3 make-index.py --root /var/lib/art-kit
Indexes lesson READMEs, book page text (Books/<Book>/page-NNN.txt), and image credits.
"""
import argparse, glob, os, re, sqlite3

ap = argparse.ArgumentParser()
ap.add_argument('--root', default=os.path.expanduser('~'), help='home dir that holds Library/')
lib = os.path.join(ap.parse_args().root, 'Library')
db = os.path.join(lib, 'index.sqlite')
tmp = db + '.new'
if os.path.exists(tmp):
    os.remove(tmp)
con = sqlite3.connect(tmp)
con.execute('CREATE VIRTUAL TABLE docs USING fts5(kind UNINDEXED, title, ref UNINDEXED, body)')
n = {'lesson': 0, 'page': 0, 'image': 0}

def add(kind, title, ref, body):
    con.execute('INSERT INTO docs VALUES (?,?,?,?)', (kind, title, ref, body))
    n[kind] += 1

for readme in sorted(glob.glob(os.path.join(lib, 'Tutorials', '*', '[0-9][0-9][0-9] *', 'README.md'))):
    d = os.path.dirname(readme)
    topic, lesson = os.path.basename(os.path.dirname(d)), os.path.basename(d)
    add('lesson', '%s · %s' % (topic, lesson), '%s/%s' % (topic, lesson), open(readme).read())

for txt in sorted(glob.glob(os.path.join(lib, 'Books', '*', 'page-*.txt'))):
    book = os.path.basename(os.path.dirname(txt))
    num = int(re.search(r'page-(\d+)', txt).group(1))
    body = open(txt, errors='replace').read()
    if body.strip():
        add('page', '%s · page %d' % (book, num), '%s/%d' % (book, num), body)

credits = os.path.join(lib, 'Inspiration', 'CREDITS.txt')
if os.path.exists(credits):
    for line in open(credits):
        p = line.rstrip('\n').split('|')
        if len(p) == 4 and not line.startswith('#'):
            add('image', p[3].split(' / ')[0], '%s/%s' % (p[0], p[1]), '%s %s' % (p[3], p[0]))

con.commit()
con.close()
os.chmod(tmp, 0o644)
os.replace(tmp, db)
print('%s: %d lessons, %d book pages, %d images' % (db, n['lesson'], n['page'], n['image']))
