#!/usr/bin/env python3
"""Make app/books-map.json: "Read:" source text -> BookName (folder in ~/Library/Books).

Usage: make-books-map.py [LESSONS_DIR] [BOOKS_TXT]
Prints every source with PDF pages that does not match a book. Exit 1 if any.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library import parse_read

here = os.path.dirname(os.path.abspath(__file__))
lessons = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'lessons')
books_txt = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, '..', 'library', 'books.txt')
STOP = {'the', 'and', 'of', 'for', 'a', 'in', 'with', 'its', 'to', 'pdf'}

def words(s):
    return {w for w in re.findall(r'[a-z0-9]+', s.lower()) if w not in STOP}

books = {}
for line in open(books_txt, encoding='utf-8'):
    if line.strip() and not line.startswith('#'):
        p = line.split('|')
        books[p[1]] = words(p[1]) | words(p[5])  # name + credit (author, title, year)

out, bad = {}, []
for readme in sorted(glob.glob(os.path.join(lessons, '*', '*', 'README.md'))):
    for line in open(readme, encoding='utf-8'):
        if line.startswith('**Read:**'):
            for src, pages in parse_read(line):
                if not pages or src in out:
                    continue
                score = sorted(((len(words(src) & w), b) for b, w in books.items()), reverse=True)
                if score[0][0] and score[0][0] > score[1][0]:
                    out[src] = score[0][1]
                elif src not in bad:
                    bad.append(src)
                    print('UNRESOLVED: %s  (%s)' % (src, os.path.relpath(readme, lessons)))

json.dump(dict(sorted(out.items())), open(os.path.join(here, 'books-map.json'), 'w', encoding='utf-8'), indent=1)
print('%d sources mapped, %d unresolved' % (len(out), len(bad)))
sys.exit(1 if bad else 0)
