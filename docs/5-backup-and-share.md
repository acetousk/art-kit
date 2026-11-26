# 5. Backup, sharing, and talking through Tresorit

For the setup adult. Sets up the backup, and turns it into a simple way for the family and the kid to talk about the art.

Tresorit is an encrypted cloud folder service (like Dropbox, but end-to-end encrypted). The kid never signs in to it on the kiosk. A service that runs as the admin user syncs the folders. The kid's account still has no network.

## The two tresors
| Tresor | On the kiosk | Kid | Parent | Way |
|---|---|---|---|---|
| **Backup** | Everything: the kid's whole home folder (art, app settings, brushes, autosaves, all files) + `/etc` kiosk config | — | **Reader: sees everything** | Kiosk → family |
| **From Family** | `~/Library/From Family` | Reads only | **Editor** (adds files) | Family → kiosk |

Rule for the kid, said out loud on day one: *"Everything on this computer, your family can see. Things we send you show up in the Library under From Family."* No hidden tracking.

## Set up (30 min)
1. Make a Tresorit account for the admin (or use yours). Make two tresors: `Backup` and `From Family`.
2. Share `Backup` with each parent as **Reader**. Share `From Family` with each parent as **Editor**.
3. On the kiosk, run `kiosk/60-backup.sh` (installs tresorit-cli, signs in as admin, syncs both tresors). `Backup` syncs the kid home except `~/Library`, plus an archive of the kiosk config files (no SSH keys, Wi-Fi, or passwords). Rebuild `~/Library` with `library/build-library.sh` on a new device. Parents can see the synced files.
4. Test: save a drawing in Krita. It shows up in the parent's Tresorit phone app in a few minutes.
5. Test: the parent puts a photo in `From Family`. It shows up in the kiosk's Library app.
6. The kid can also get their own files on a phone or school laptop: share `Backup` with the kid's own Tresorit account (Reader).

The backup timer copies only `.png`, `.jpg`, `.jpeg`, `.pdf`, and `.txt` files from `From Family` to the read-only `~/Library/From Family` folder (`~/Library` links to `/var/lib/art-kit/Library`, outside the kid home).

## Using it to understand what your kid is doing
| What you want | How Tresorit shows it |
|---|---|
| **Where they are in the course** | Files are named by topic and lesson: `Backup/Art/Drawing/023 …`, `Backup/Art/Interior Design/My-Bedroom/…`. The newest folder is the current lesson. |
| **What they did today** | The daily job (`kiosk/70-daily.sh`) writes `Backup/Art/Daily/<date>.html`: lessons opened, files saved, time in each app. The kid can open it too. |
| **How a piece grew** | Each save is a new version. Open a file's **version history** to see the steps, from sketch to finished. |
| **What they made this week** | Sort `Backup` by date in the Tresorit app. |

## Using it to talk
| Idea | How |
|---|---|
| **Send a drawing prompt** | Put a photo in `From Family` (the dog, a room, a sunset). Name it what you want: `Draw this - our dog.jpg`. |
| **Send a "client" brief** | For the Design and Interior Design projects: a short note or a photo of a handwritten brief. "Design a poster for Grandma's birthday." "Redo the guest room: calm, blue, a desk." |
| **Give feedback** | Write on a printout or a sticky note, take a photo, and put it in `From Family`. Or draw on a copy of their art in a phone drawing app and send that. Start with what you like. |
| **Kid replies** | The kid draws or writes a note in Krita and saves it in `Backup/Art/Notes/`. The Library app also has a **Note** box that saves `Backup/Art/Notes/<date>.txt`. |
| **Show the grandparents** | Make a Tresorit **share link** to one finished file or folder, with a password and an end date. Only that item is shared. |
| **A weekly look together** | Sit with your kid and the Tresorit app for 10 minutes. Ask them to show one file's version history and explain the steps. |

## Good habits
- Look, but do not comment on every file. Pick one piece a week.
- Ask before you share outside the family.
- No screen watching. The daily page shows what was made, not a live view.
- If a file is deleted by mistake, restore it from Tresorit's version history (or deleted files).
- If the device breaks, install the kit on a new one and copy `Backup` back. Everything returns: art, settings, brushes.
