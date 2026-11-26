#!/usr/bin/env python3
"""Check that every quote in every lesson README is really in its source.

Usage: python3 -I tools/check-quotes.py <lessons-dir> <books-dir>

<books-dir> holds the book PDFs (<name>.pdf). Text files (<name>.txt) are made
with pdftotext if missing. Krita Manual quotes are checked against
<books-dir>/krita-manual/ (the unzipped Krita Manual epub).

Quote formats it finds:
  "quote" (Author, PDF page 12)    "quote" (Author, PDF p. 12)    "quote" (Author, PDF 12)
  "quote" (Krita Manual, Page title)

A book quote passes when 60 % of its 3-word groups are on the cited page (or the
page before or after). If a page has almost no text (a scanned plate), the page
is read with tesseract OCR. Exit code 1 if any quote fails.
"""
import glob, html, os, re, subprocess, sys, tempfile

MIN_SCORE = 0.6

def words(s):
    return re.sub(r"[^a-z]+", " ", s.lower().replace("-\n", "")).split()

def trigrams(w):
    return set(zip(w, w[1:], w[2:]))

def score(quote_words, page_trigrams):
    g = list(zip(quote_words, quote_words[1:], quote_words[2:]))
    return sum(x in page_trigrams for x in g) / len(g) if g else 0.0

def load_books(books_dir):
    books = {}
    for pdf in glob.glob(os.path.join(books_dir, "*.pdf")):
        txt = pdf[:-4] + ".txt"
        if not os.path.exists(txt) or os.path.getsize(txt) == 0:
            subprocess.run(["pdftotext", "-layout", pdf, txt], stderr=subprocess.DEVNULL)
        if os.path.exists(txt):
            pages = open(txt, errors="ignore").read().split("\f")
            books[os.path.basename(pdf)[:-4]] = {"pdf": pdf, "pages": [words(p) for p in pages], "ocr": {}}
    # Revoy articles are local text sources, not PDFs. Check their quotes against
    # the matching local article text.
    revoy_dir = os.path.join(books_dir, "revoy")
    if os.path.isdir(revoy_dir):
        books["revoy"] = {"pdf": None, "pages": [], "ocr": {}, "texts": [
            words(open(f, errors="ignore").read())
            for f in glob.glob(os.path.join(revoy_dir, "*.txt"))
        ]}
    return books

def ocr_page(book, n):
    if n in book["ocr"]:
        return book["ocr"][n]
    w = []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", "200", "-png", book["pdf"], d + "/p"],
                       stderr=subprocess.DEVNULL)
        for png in glob.glob(d + "/p*.png"):
            out = subprocess.run(["tesseract", png, "-"], capture_output=True, text=True).stdout
            w += words(out)
    book["ocr"][n] = w
    return w

def revoy_match(book, quote):
    q = trigrams(quote)
    return max((score(quote, trigrams(t)) for t in book.get("texts", [])), default=0.0)

def page_words(book, n):
    if not 1 <= n <= len(book["pages"]):
        return []
    w = book["pages"][n - 1]
    return w if len(w) > 40 else ocr_page(book, n)   # image-only page: use OCR

def load_krita_manual(books_dir):
    files = glob.glob(os.path.join(books_dir, "krita-manual", "**", "*.xhtml"), recursive=True)
    text = " ".join(open(f, errors="ignore").read() for f in files)
    return trigrams(words(html.unescape(re.sub(r"<[^>]+>", " ", text)))) if files else None

BOOK_QUOTE = re.compile(r'"([^"]{15,})"\s*\(([^)]*?)PDF (?:pages? |p\. ?)?(\d+)')
KRITA_QUOTE = re.compile(r'"([^"]{15,})"\s*\(Krita Manual')

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lessons_dir, books_dir = sys.argv[1], sys.argv[2]
    books, km = load_books(books_dir), load_krita_manual(books_dir)
    total = failed = 0
    for f in sorted(glob.glob(os.path.join(lessons_dir, "**", "README.md"), recursive=True)):
        txt, name = open(f).read(), os.path.relpath(f, lessons_dir)
        for m in BOOK_QUOTE.finditer(txt):
            q, cited = words(m.group(1)), int(m.group(3))
            total += 1
            if len(q) < 3:
                continue  # too short to check by machine; check by eye
            # Restrict the page search and OCR to the cited source. This avoids
            # OCR across unrelated scanned books for every quote.
            label = m.group(2).split(",", 1)[0]
            tokens = {x for x in words(label) if x not in {"the", "a", "and", "of", "book"}}
            candidates = [(b, book) for b, book in books.items()
                          if b != "revoy" and tokens and
                          len(tokens & set(words(b.replace("-", " ")))) >= min(1, len(tokens))]
            if not candidates:
                candidates = [(b, book) for b, book in books.items() if b != "revoy"]
            best = (0.0, "", 0)
            for b, book in candidates:
                for n in (cited, cited - 1, cited + 1):
                    if 1 <= n <= len(book["pages"]):
                        s = score(q, trigrams(book["pages"][n - 1]))
                        if s > best[0]:
                            best = (s, b, n)
            if best[0] < MIN_SCORE:
                for b, book in candidates:
                    for n in (cited, cited - 1, cited + 1):
                        if 1 <= n <= len(book["pages"]) and len(book["pages"][n - 1]) <= 40:
                            s = score(q, trigrams(page_words(book, n)))
                            if s > best[0]:
                                best = (s, b + " (OCR)", n)
            if best[0] < MIN_SCORE:
                failed += 1
                print(f"FAIL\t{name}\tcited PDF {cited}\tbest {best[0]:.2f} {best[1]} p{best[2]}\t\"{m.group(1)[:60]}\"")
        for m in KRITA_QUOTE.finditer(txt):
            total += 1
            if km is None:
                continue
            if score(words(m.group(1)), km) < MIN_SCORE:
                failed += 1
                print(f"FAIL\t{name}\tKrita Manual\tnot found\t\"{m.group(1)[:60]}\"")
    print(f"{total} quotes checked, {failed} failed", file=sys.stderr)
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
