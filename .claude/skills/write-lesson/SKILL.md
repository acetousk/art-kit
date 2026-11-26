---
name: write-lesson
description: Write, check, and fix Art Kit lessons with the user. Use when the user says "write a lesson", "new lesson", "add a lesson", "make a tutorial", "review lessons", or "check lessons" in the Art Kit repo.
---

# Write a lesson

One lesson = one folder `lessons/<Topic>/<NNN Title>/README.md`, in the template in `lessons/RULES.md`. The kid opens it in the Library app on the kiosk. Read `lessons/RULES.md` and 2 lessons near the new one before you start.

## What "good enough" means
Short lessons with 3–5 vague steps were rejected. A good lesson:
- Teaches **one idea from a real artist or designer**, in plain words, with a short real quote and a real page.
- Has 8–15 steps. Each step is one action with the **exact** menu, tool, or docker name.
- Says "You should see: …" after hard steps.
- Makes a named file in `~/Art/<Topic>/`. "Builds on" links the earlier file in a project chain.
- Has 3 "Check your work" questions about the idea, not about saving.
- Fits its place in the course: easy → hard, and a project lesson every ~8 lessons.

## Hard rules
| Rule | Why |
|---|---|
| Never invent a page, quote, menu, tool, brush preset, or shortcut. If you cannot check it, leave it out. | Writers guessed menu paths and preset names. A wrong name stops a 13-year-old. |
| Teaching comes from a real source: a book, a manual, or a named artist's files. Do not make up your own method. | The kit teaches from existing designers and artists. |
| Open sources only: public domain, CC0, CC BY, CC BY-SA, GNU FDL. Use a paid source only if no good open one exists, and ask the user first. | Anyone can install the kit for free. |
| Steps work **offline on the kiosk**: Krita, Sweet Home 3D, Blender, and the Library app only. No browser, no PDF viewer, no timer or clock app, no downloads, no add-ons. | The kid account has no network and no other apps. |
| Book pages are shown **only in the Library app** (as page images). Write "Open the book page in the Library", never "open the PDF". | There is no PDF viewer. |
| Physical items (tape measure, mirror, cup) are OK. List them at the top: `**You need:** …`. | The kid must know before starting. |
| Nothing unsuitable for kids. Skip nude pages (Bridgman: hands, arms, head, face, legs, feet, skeleton only). Skip dated social opinions. | Old books need cleaning. |
| No personal names, towns, or accounts in any file. | The repo is public. |
| Keep it simple. Change as few lines as needed. Keep the template. | KISS. |

## App versions
- Krita: use the version Fedora ships. Check it:
  `curl -s https://mdapi.fedoraproject.org/f44/pkg/krita | python3 -c "import json,sys;print(json.load(sys.stdin)['version'])"`
  (Fedora 44+ ships Krita 6.0.) Use only features in that version.
- The Krita Manual (`docs.krita.org`, epub) shows the newest version. If a feature is newer than the device's Krita, leave it out.
- Sweet Home 3D: use the names in the Sweet Home 3D User's Guide.
- Brush presets: use a preset name only if the Krita Manual names it (for example "Ink Fineliner"). Otherwise write "a pencil brush preset".

## Steps
1. Ask the user: the topic, the learner's age and level, the idea to teach, and what the learner will make.
2. Ask for the source, or find one in `library/books.txt`. Check the license.
3. Find the place in `lessons/COURSE.md` (unit and order). Find the next free `NNN` in `lessons/<Topic>/`.
4. Read the source pages. Use **PDF page numbers**, not printed page numbers:
   `pdftotext -f N -l N -layout <book>.pdf -`
5. For a picture page or a scanned plate, look at it. Text extraction misses captions:
   `pdftoppm -f N -l N -r 100 -png <book>.pdf /tmp/p` and view the PNG, or OCR it with `tesseract /tmp/p-N.png -`.
6. Pick a quote of max 25 words. Copy it word for word. Format: `"quote" (Author, PDF page N)`.
7. Check every app name in the Krita Manual or the Sweet Home 3D Guide. Write the exact name.
8. Write the README in the template. Fill "You make", "Builds on", "Time", and "Read".
9. Make the last step save to the "You make" path. For a project chain, step 1 opens the earlier file.
10. If the source is new, add one line to `library/books.txt`: `folder|name|url|pages|remove pages|credit`.
11. Add the lesson to `lessons/COURSE.md`.
12. Run the checks below. Then do the review.

## Checks (run all)
```
python3 -I tools/check-quotes.py lessons /path/to/books
```
- `check-quotes.py` checks every quote against its cited PDF page (page ±1), and Krita Manual quotes against the manual. It uses OCR for image-only pages. It is slow on scans (minutes).
- A FAIL near 0.5–0.6 on the right page is usually a scan typo, an ellipsis (`…`), or a line break. Check it by eye.
- A FAIL near 0 means the quote is on another page or not in the book. Fix the page or replace the quote.

| Check | Pass when |
|---|---|
| Quote | `check-quotes.py` passes, or you checked it by eye on the page image |
| Pages | Each page in "Read" teaches the idea of the lesson |
| App names | Each menu, tool, docker, preset, and shortcut is in the manual for the device's version |
| Offline | No browser, PDF viewer, timer, download, or add-on |
| Steps | 8–15 steps, one action each, max 20 words, in a working order |
| "You should see" | True for what the app really shows |
| Files | "You make" and "Builds on" match earlier lessons; the last step saves there |
| Age 13 | Plain words; max 3 new words, each with a meaning |
| Safety | No nude pages, no unsuitable images or opinions |
| Privacy | No personal names, towns, or accounts |

## Review (critique and fix in one pass)
A review that only reads a sample and says "no issue" is not enough. Do this:
1. Pick a random sample: `python3 -c "import random,glob; random.seed(S); print(random.sample(sorted(glob.glob('lessons/*/*/README.md')), K))"`. Record the seed. Use about 6 per topic.
2. For each sampled lesson, do every check in the table. Open the real page. Look up every app name.
3. Read the steps as a 13-year-old. Ask at each step: "Can I do this now, on this tablet, with only these words?"
4. Fix each lesson in place.
5. **If an issue is a pattern**, fix it in every file, not only the sample. Find it with `grep -rn "<pattern>" lessons/`. Examples: a wrong menu path, a preset name, a newer-version feature, "open the PDF", a timer, a wrong save path, a page offset for one book.
6. Run `check-quotes.py` on all lessons.
7. Write `lessons/REVIEW.md`: seed and sample; a table `Lesson | Issue | Severity | Fix`; patterns fixed with file counts; what you could not fix and why.

## Report to the user
- The lesson path(s).
- Anything you could not check (a page, a menu name), and why.
- What needs a test on the real device.
