---
name: fork-kit
description: Fork the Art Kit and make it your own - topics, books, images, lessons, device. Use when the user says "fork", "make my own kit", "customize the kit", "my own lessons", "add a topic", or "different device" in the Art Kit repo.
---

# Fork the kit

Help a family or a teacher make their own copy of the Art Kit. Keep it simple: change only what they ask for. Do not commit or open a pull request until the user asks.

## Hard rules
| Rule | Why |
|---|---|
| Never commit real names, towns, schools, photos, Wi-Fi passwords, or account details. | Forks are public. |
| `kit.conf` holds nicknames only. Real values go on the device only. | Same. |
| Books and lessons: open sources only (public domain, CC0, CC BY, CC BY-SA, GNU FDL). Paid only if no good open source exists, and only with the user's OK. | Anyone can install the kit for free. |
| Images: CC0 or public domain only. Check each one for age fit. | Museum collections include nudes and adult scenes (for example some Japanese courtesan prints). |
| The family sees everything on the device (Tresorit backup of the whole home). Tell the kid on day one. | No hidden tracking. |

## Steps: start a fork
1. Fork and clone: `gh repo fork acetousk/art-kit --clone && cd art-kit`. This also adds the `upstream` remote.
2. Edit `kit.conf`: `KID`, `ADMIN`, `HOST` (nicknames), and `SURFACE=yes` only for a Microsoft Surface.
3. Keep or drop topics: delete a topic folder in `lessons/`. Remove its section from `lessons/COURSE.md`.
4. Books: edit `library/books.txt` (`folder|name|url|pages|remove pages|credit`). To drop a book, delete its line. Drop the lessons that cite it too: `grep -rl "<book>" lessons/`.
5. Images: edit `library/inspiration.txt` (`collection|file|url|credit`). See "Add images" below.
6. Install: follow `docs/1-get-a-device.md`, then run `sudo kiosk/install.sh` on a fresh Fedora.

## Add a whole new topic
1. **Sources first.** Find 2–5 open sources by real artists or designers: old books (archive.org, public domain), open manuals (Krita, Blender), open textbooks, or an artist's CC BY files.
   - Check each license. Write it down.
   - Read the table of contents. Check that the book teaches what the topic needs.
   - Check it for age 13. List pages to remove in the `remove pages` field.
2. Add each source to `library/books.txt`.
3. **Units.** Add a section to `lessons/COURSE.md`: a table `Unit | Lessons | Source | License`. Order easy → hard. Plan a project lesson every ~8 lessons.
4. **Lessons.** Use the `write-lesson` skill for each lesson. Number them `001`, `002`, … in `lessons/<Topic>/`.
5. **App.** If the topic needs a new app, add it to `kiosk/install.sh` (Flatpak with `--unshare=network`) and to the dock. Test it in a VM first.
6. **Review.** Do the review in `write-lesson` (critique and fix, fix patterns across all files). Run `python3 -I tools/check-quotes.py lessons <books-dir>`.

## Add images (Inspire)
1. Use museum open-access collections with CC0 images (for example the Art Institute of Chicago, the Met, Cooper Hewitt, Smithsonian).
2. Add lines to `library/inspiration.txt`.
3. Make a contact sheet and look at every image before it goes in:
   `montage <dir>/*.jpg -tile 8x -geometry 200x200+4+4 sheet.jpg` (ImageMagick), then view `sheet.jpg`.
4. Remove nudes, violence, war propaganda, and adult scenes. When in doubt, remove it.

## Use a different device
- Read `docs/1-get-a-device.md`. Wacom-pen 2-in-1s work best. A Surface needs a genuine Microsoft pen and `SURFACE=yes`. A laptop + USB Wacom tablet is cheapest.
- Before you pay: boot the Fedora Live USB, run `tools/device-check.sh`, and test the pen in `tools/pen-test.html` (pressure must change from light to hard).
- Chromebooks, iPads, Android tablets, Macs, and ARM laptops do not work.

## Stay up to date
```
git fetch upstream
git merge upstream/master
```
If a merge conflicts, keep your own `kit.conf`, `library/*.txt` choices, and lessons. Take upstream's fixes to scripts and tools.

## Send a good lesson upstream
1. Make a branch from upstream: `git checkout -b add-<lesson> upstream/master`.
2. Copy in only the lesson folder, its `books.txt` line, and its `COURSE.md` line.
3. Check privacy: `grep -rniE "<your names>|<town>|<school>" .` must find nothing. No photos of people.
4. Check quality: all `write-lesson` checks pass. Run `tools/check-quotes.py`.
5. Ask the user before you push. Then `git push -u origin add-<lesson>` and `gh pr create -R acetousk/art-kit`.
6. In the PR: the idea, the source and license, and what you tested on a real device.
