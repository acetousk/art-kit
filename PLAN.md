# Art Kit: plan and repo layout

A kit that other families can install. It turns a cheap laptop or tablet with a pen into a safe, offline art computer for a kid. It comes with a year of art lessons and a library of open books and museum images.

## Goal
| | |
|---|---|
| **For** | Kids 12–16 who like to draw, design, or decorate rooms |
| **Device** | Any x86 laptop or tablet with a pen (example: used Surface Pro 5 + pen, about $160) |
| **Result** | Turn it on → kid is in Krita. Dock: Krita · Sweet Home 3D · Blender · Library. No web, no store, no settings. |
| **Lessons** | ~305 lessons in 7 topics, from age 13 to professional level, all from open sources |
| **Adults** | A **parent** (no tech needed) and a **setup adult** (comfortable with computers). Can be the same person. |
| **Cost** | Device only. All software, books, lessons, and images are free. Optional: Tresorit (backup) and Tailscale (remote help). |

## Repo layout
```
art-kit/
├── README.md              What it is, who reads what, the rules
├── PARENTS.md             For parents: everything, no tech needed
├── kit.conf               The only file you edit: kid name, admin name, Wi-Fi, options
├── install.sh             Runs every step below in order (as root, on a fresh Fedora)
├── docs/
│   ├── 1-get-a-device.md      What to buy, what works, pen tests before you pay
│   ├── 2-install-fedora.md    USB stick, install, first boot
│   ├── 3-run-the-kit.md       Edit kit.conf, run install.sh, the manual steps
│   ├── 4-first-day.md         Kid's first hour: dock, pen, first lesson, saving
│   ├── 5-backup-and-share.md  Whole-device backup; parents see everything (Tresorit)
│   ├── 6-remote-help.md       Tailscale + T3 Code for the setup adult (optional)
│   ├── 7-maintenance.md       Updates, health checks, rollback, adding lessons
│   └── 8-when-stuck.md        Problems and fixes
├── kiosk/                 The locked-down system
│   ├── 10-hardware.sh         linux-surface (only if a Surface), pen driver
│   ├── 20-kiosk.sh            GNOME Kiosk session, autologin, dock, VT lock
│   ├── 30-lockdown.sh         No network for the kid, USB storage off, Krita Python off
│   ├── 40-apps.sh             Krita, Sweet Home 3D, Blender (Flatpak, no network)
│   ├── 50-admin.sh            Admin user, auto updates (no auto reboot), Tailscale, T3 Code
│   ├── 60-backup.sh           Tresorit sync of the whole home + /etc (optional)
│   ├── dock/                  The dock bar app (Python + GTK)
│   └── tests.sh               Checks: autologin, no network, USB block, dock, apps
├── library/
│   ├── books.txt              19 open books: name | url | pages | pages removed | credit
│   ├── inspiration.txt        Museum images: collection | file | url | credit
│   ├── revoy.txt              Pepper&Carrot files and brushes to download
│   ├── videos.txt             Blender Grease Pencil videos
│   ├── build-library.sh       Downloads everything into ~/Library (read-only)
│   └── CREDITS.md             Every source, author, and license
├── lessons/
│   ├── RULES.md               How a lesson is written (template)
│   ├── COURSE.md              The full course map: topic → unit → lesson → app → source
│   ├── Drawing/001 …/README.md    One folder per lesson
│   ├── Painting/ … Revoy/ … Design/ … Lettering/ … Interior Design/ … 3D Drawing/
│   └── tools/make-index.py    Builds COURSE.md and the search index
├── app/                   The Library app (Tutorials + Inspire + search)
│   ├── library-app.py         Python + GTK + WebKit, offline only
│   └── ui/                    Local HTML/CSS
└── vmtest/                Test the whole kit in a VM before a real device
    ├── run-vm.sh
    └── REPORT.md
```

## Who reads what
| Who | Reads |
|---|---|
| Parent | `PARENTS.md` |
| Setup adult | `docs/1` → `docs/3`, then `docs/5`–`docs/8` |
| Kid | `docs/4-first-day.md`, then the Library app |
| Lesson writers | `lessons/RULES.md` |

## Build plan
| # | Work | Done when |
|---|---|---|
| 1 | Move the current setup script into `kiosk/` steps; read names from `kit.conf` | `install.sh` runs on a fresh Fedora VM |
| 2 | Read names from `kit.conf`; Surface parts optional | No personal names in the repo |
| 3 | Finish the VM test; fix the kiosk | `kiosk/tests.sh` all pass |
| 4 | Library download script with checksums | `~/Library` builds offline-ready |
| 5 | Lessons v2 + review; add Revoy and 3D Drawing | 305 lessons pass review |
| 6 | Library app | Tutorials, Inspire, and search work in the VM |
| 7 | Docs + PARENTS.md | A second adult installs it from the docs only |
| 8 | Real device test | A kid uses a real device for 2 weeks |
| 9 | v1 release | A second family installs it from the docs |

## Rules for the repo
- No personal names, no home towns, no accounts in the repo. All personal data goes in `kit.conf` on the device only.
- Only open content: public domain, CC0, CC BY, CC BY-SA, GNU FDL. Every item is in `CREDITS.md`.
- The repo has the download list, not the books (the books are big; the list keeps the repo small).
