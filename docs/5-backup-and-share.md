# 5. Backup, sharing, and talking through Tresorit

For the setup adult. Sets up the backup, and turns it into a simple way for the family and the kid to talk about the art.

Tresorit is an encrypted cloud folder service (like Dropbox, but end-to-end encrypted). The kid never signs in to it on the kiosk. A service that runs as the admin user syncs the folders. The kid's account still has no network.

## The three folders ("tresors")
| Tresor | On the kiosk | Kid | Parent | Way |
|---|---|---|---|---|
| **Backup** | Everything: the kid's whole home folder (art, app settings, brushes, Krita autosaves, Sweet Home 3D and Blender files) + `/etc` kiosk config | — | Admin only | Kiosk → cloud |
| **Art** | `~/Art` | Writes | **Reader** (sees all) | Kiosk → family |
| **From Family** | `~/Library/From Family` | Reads only | **Editor** (adds files) | Family → kiosk |

Rule for the kid, said out loud on day one: *"Everything in Art, your family can see. Things we send you show up in the Library under From Family."* No hidden tracking.

## Set up (30 min)
1. Make a Tresorit account for the admin (or use yours). Make three tresors: `Backup`, `Art`, and `From Family`.
2. Share `Art` with each parent as **Reader**. Share `From Family` with each parent as **Editor**.
3. On the kiosk, run `kiosk/60-backup.sh` (installs tresorit-cli, signs in as admin, syncs all three tresors). `Backup` syncs everything, so a new device can be restored in one step.
4. Test: save a drawing in Krita. It shows up in the parent's Tresorit phone app in a few minutes.
5. Test: the parent puts a photo in `From Family`. It shows up in the kiosk's Library app.
6. The kid can also get their own files on a phone or school laptop: share `Art` with the kid's own Tresorit account (Reader).

Only images (`.png .jpg`), PDFs, and `.txt` notes from `From Family` are shown in the Library. Other file types are ignored.

## Using it to understand what your kid is doing
| What you want | How Tresorit shows it |
|---|---|
| **Where they are in the course** | Files are named by topic and lesson: `Art/Drawing/023 …`, `Art/Interior Design/My-Bedroom/…`. The newest folder is the current lesson. |
| **What they did today** | A nightly job writes `Art/Daily/<date>.html`: lessons opened, files saved, time in each app. The kid can open it too. |
| **How a piece grew** | Each save is a new version. Open a file's **version history** to see the steps, from sketch to finished. |
| **What they made this week** | Sort `Art` by date in the Tresorit app. |

## Using it to talk
| Idea | How |
|---|---|
| **Send a drawing prompt** | Put a photo in `From Family` (the dog, a room, a sunset). Name it what you want: `Draw this - our dog.jpg`. |
| **Send a "client" brief** | For the Design and Interior Design projects: a short note or a photo of a handwritten brief. "Design a poster for Grandma's birthday." "Redo the guest room: calm, blue, a desk." |
| **Give feedback** | Write on a printout or a sticky note, take a photo, and put it in `From Family`. Or draw on a copy of their art in a phone drawing app and send that. Start with what you like. |
| **Kid replies** | The kid draws or writes a note in Krita and saves it in `Art/Notes/`. The Library app also has a **Note** box that saves `Art/Notes/<date>.txt`. |
| **Show the grandparents** | Make a Tresorit **share link** to one finished file or folder, with a password and an end date. Only that item is shared. |
| **A weekly look together** | Sit with your kid and the Tresorit app for 10 minutes. Ask them to show one file's version history and explain the steps. |

## Good habits
- Look, but do not comment on every file. Pick one piece a week.
- Ask before you share outside the family.
- No screen watching. The daily page shows what was made, not a live view.
- If a file is deleted by mistake, restore it from Tresorit's version history (or deleted files).
- If the device breaks, install the kit on a new one and copy `Backup` back. Everything returns: art, settings, brushes.
