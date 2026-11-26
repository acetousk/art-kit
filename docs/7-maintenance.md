# 7. Maintenance

For the setup adult. Do the checks below. Use Tailscale SSH from your computer, or work at the device as `$ADMIN`.

## 1. Weekly checklist (10 min)

| Check | Command or place | You should see |
|---|---|---|
| Failed services | `systemctl --failed` | `0 loaded units listed` |
| Disk space | `df -h /` | Use under 85 % |
| Backup date | Tresorit app, **Backup** (see section 6) | A file from this week |
| Kid's work | Ask the kid to show one file | The file opens in Krita |

## 2. Monthly checklist (20 min)

| Check | Command | You should see |
|---|---|---|
| Automatic updates timer | `systemctl list-timers dnf5-automatic.timer` | A next run time |
| Battery health | `bash tools/device-check.sh` (run in the kit folder) | Battery 70 % or more |
| Pen | Draw a slow line in Krita | No gaps |
| Updates applied | `sudo dnf history` | A recent upgrade entry |

## 3. Automatic updates

`install.sh` step 10 turns on `dnf5-automatic`. Updates install on their own.

| Setting | Value |
|---|---|
| Apply updates | Yes (`apply_updates = yes`) |
| Reboot | Never (`reboot = never`) |

The device does not restart by itself. You restart it (section 4). `dnf5-plugins` provides the `needs-restarting` command on Fedora 44.

## 4. Reboot safely

1. Tell the kid to save their work. Krita closes at restart.
2. Plug in the charger.
3. Check that no update runs. Run `systemctl is-active dnf5-automatic.service`. You should see `inactive`.
4. Restart: `sudo systemctl reboot`.
5. Check the kiosk. Krita must open.

Restart after a core update. Run `sudo dnf install -y dnf5-plugins`. Then run `sudo dnf needs-restarting -r`. If it says a reboot is needed, do steps 1 to 5.

## 5. Fedora version upgrade (every 6 months)

Fedora releases in April and October. Upgrade only after the Surface kernel repo supports the new release (Surface only). Replace `<N>` with the new Fedora number.

```sh
sudo dnf upgrade --refresh -y
sudo dnf system-upgrade download --releasever=<N> -y
sudo dnf offline reboot
```

**You should see:** the device restarts and installs the upgrade.

After the upgrade, run the tests in [3-run-the-kit.md](3-run-the-kit.md), section 6.

## 6. Backup health

The Backup tresor is set up with Tresorit. See [5-backup-and-share.md](5-backup-and-share.md).

1. Open the Tresorit app. Open the **Backup** tresor.
2. Check the newest file date.
3. Save a drawing in Krita. Wait 5 minutes. The file must appear in Backup.

## 7. Snapshots

The kit does not make btrfs snapshots. To check, run `sudo btrfs subvolume list /`. If no snapshot is listed, skip this section. For rollback, use the kernel menu in [8-when-stuck.md](8-when-stuck.md).

## 8. Add lessons and images

Only add open content: public domain, CC0, CC BY, CC BY-SA, or GNU FDL. See [README.md](../README.md).

### Add a lesson

1. In the repo, put the lesson folder in `lessons/<Topic>/`. Name it `NNN Title`.
2. Check the quotes: `python3 tools/check-quotes.py lessons`.
3. Run `sudo bash library/build-library.sh` to copy lessons into `/var/lib/art-kit/Library/Tutorials/`.
4. The script makes Library read-only:

```sh
sudo chown -R root:root /var/lib/art-kit/Library
sudo chmod -R a+rX,go-w /var/lib/art-kit/Library
```

**You should see:** the new lesson in the Library.

### Add an Inspire image

1. Add one line to `library/inspiration.txt`. Use this format: `dir|file|url|credit`.
2. Run `sudo bash library/build-library.sh` to download it.

## 9. Replace the pen battery

The Surface Pen 1776 uses one AAAA battery.

1. Get a new AAAA battery.
2. Open the pen as shown in the Microsoft Surface Pen guide for model 1776.
3. Put in the new battery. Point the + end toward the pen tail. If the top button stops working, replace its two size 319 coin cells too.
4. Close the pen. Test it in Krita.

## Checklist

- [ ] Weekly checks done.
- [ ] Monthly checks done.
- [ ] Reboot done when needed (section 4).
- [ ] Backup checked (section 6).
