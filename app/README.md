# Library app

One full-screen window for the kid: **Tutorials**, **Inspire**, **From Family**, **Note**, and search.
Python 3 + GTK 4 + WebKitGTK 6. The UI is local HTML in `ui/`. All data comes from Python through the
`library://` URI scheme. There is no web server and no port. The app blocks all http, https, and file
loads, dev tools, the right-click menu, downloads, and new windows.

## Files

| File | Use |
|---|---|
| `library-app.py` | The window (GTK + WebKit). Option `--root DIR` (default: your home) |
| `library.py` | Backend: lessons, pages, images, notes, search. No GTK, so you can test it alone |
| `ui/` | `index.html`, `style.css`, `app.js` |
| `books-map.json` | "Read:" source text → book folder in `~/Library/Books/` |
| `make-books-map.py` | Makes `books-map.json` from `../library/books.txt` and `../lessons`. Prints unresolved sources |
| `make-index.py` | Makes the search index `~/Library/index.sqlite` (SQLite FTS5) |
| `library.desktop` | Launcher for the dock |

## What it reads and writes

| Path | Use |
|---|---|
| `~/Library/Tutorials/<Topic>/<NNN Title>/README.md` | Lessons |
| `~/Library/Books/<Book>/page-NNN.png` and `.txt` | Book pages (NNN = PDF page number) and their text |
| `~/Library/Inspiration/<collection>/` + `CREDITS.txt` | Images. Credit lines: `folder\|file\|url\|credit` |
| `~/Library/From Family/` | Images, `.txt`, and `.pdf` (first page) |
| `~/Art/.library-log` | One line per finished lesson: `ISO-time<TAB>Topic/NNN Title` |
| `~/Art/Favorites/`, `~/Art/Notes/` | Saved images and notes |
| `~/.cache/library/` | PDF first-page images |

## Install (as admin)

1. Install the packages: `sudo dnf install -y python3-gobject gtk4 webkitgtk6.0 python3-markdown poppler-utils`
2. Copy the app: `sudo mkdir -p /opt/art-kit && sudo cp -r app /opt/art-kit/`
3. Install the launcher: `sudo cp /opt/art-kit/app/library.desktop /usr/share/applications/`
4. After each library update, build the search index: `sudo python3 /opt/art-kit/app/make-index.py --root /var/lib/art-kit`
5. Make the index readable: `sudo chmod a+r /var/lib/art-kit/Library/index.sqlite`

When you add lessons that cite a new book, run `python3 make-books-map.py`. Fix every UNRESOLVED line.

## Run

- Kid: tap **Library** in the dock. The dock runs the `Exec` line of `library.desktop`.
  If the app is already open, the dock tap shows the open window (one app instance).
- Test on a test library: `python3 library-app.py --root /tmp/libtest`
  (`/tmp/libtest` holds `Library/` and `Art/`).
- Close: Alt+F4 or the dock. Esc or **Back** goes back one screen.
