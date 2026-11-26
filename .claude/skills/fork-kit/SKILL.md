---
name: fork-kit
description: Fork the Art Kit and make it your own. Use when the user says "fork", "make my own kit", "customize the kit", or "my own lessons" in the Art Kit repo.
---

# Fork the kit

Use this skill to help a family or teacher make their own copy of the Art Kit.

## Hard rules

- Never commit real names, towns, photos, Wi-Fi passwords, or account details.
- Use nicknames in `kit.conf`. Do not commit real values.
- Use only open sources for books. Use public domain, CC0, CC BY, CC BY-SA, or GNU FDL.
- Use only CC0 or public domain images.
- Check each image for age fit before you keep it.
- Do not commit or open a pull request until the user asks.

## Steps

1. Fork the repo and clone it: `gh repo fork acetousk/art-kit --clone`.
2. Go into the new folder: `cd art-kit`.
3. Open `kit.conf`. Set `KID`, `ADMIN`, `HOST`, and `SURFACE`. Use nicknames.
4. Choose topics. To drop a topic, delete its folder in `lessons/`. Update `lessons/COURSE.md` to match.
5. Edit `library/books.txt`. Delete a line to drop a book.
6. To add a book, add one line: `folder|name|url|pages|remove|credit`.
7. Edit `library/inspiration.txt`. Delete a line to drop an image.
8. To add an image, add one line: `folder|file|url|credit`. Check the license first.
9. Add lessons with the `write-lesson` skill. Put each lesson in `lessons/<Topic>/`.
10. Test the kit in a VM before a real device (`vmtest/`, coming in a later version).
11. Check that the kid account has no network in the VM.
12. Install on the device. On a fresh Fedora install, run `sudo kiosk/install.sh`.
13. Keep the kit up to date: `git fetch upstream && git merge upstream/master`.
14. If a merge conflicts, keep your own `kit.conf` and list edits.
15. To send a good lesson upstream, make a branch: `git checkout -b add-<lesson-name>`.
16. Commit only the lesson folder, its `books.txt` line, and its `COURSE.md` line.
17. Check the lesson for names, towns, and photos of children. Remove any you find.
18. Open a pull request with `gh pr create`. Describe the lesson in one paragraph.

## Keep private data out

| Put here | Do not put here |
|---|---|
| Nicknames in `kit.conf` on the device | Real names in any repo file |
| Open sources in `library/` | Photos of the kid or family |
| Lessons with no personal data | Wi-Fi passwords or account logins |
| Public domain or CC0 images | Copyrighted images |

## Make a good lesson for upstream

- Pass every check in `write-lesson`.
- Use one topic only.
- Keep steps that work offline on the kiosk.
- Cite the source and page for every idea.
