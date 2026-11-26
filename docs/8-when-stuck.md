# 8. When stuck

For the setup adult and the kid. Find the problem in the first column. Do the check. Then do the fix. Run the tests in [3-run-the-kit.md](3-run-the-kit.md), section 6, after each fix.

Use Tailscale SSH from your computer for remote checks: `ssh $ADMIN@$HOST`.

| Problem | Check | Fix |
|---|---|---|
| **Pen does not work** | Surface: `uname -r` shows `.surface.`. Run `systemctl list-units 'iptsd@*'`. You should see one unit, `active running`. | Restart: `sudo systemctl restart 'iptsd@*'`. Restart the device. If the Fedora kernel boots, pick the newest `.surface.` kernel in the boot menu (hold **Shift** or press **Esc**). |
| **Pen flicker** (gaps in lines) | Draw a slow line for 30 seconds. | Surface: see [iptsd issue 195](https://github.com/linux-surface/iptsd/issues/195). Tell the setup adult. |
| **Screen flicker** | Does it happen in every app? | Restart the device. If it returns, write down the app and the time. Tell the setup adult. |
| **App gone** (Krita) | `rpm -q krita` | `sudo dnf install -y krita` |
| **App gone** (Sweet Home 3D, Blender) | Install with `sudo flatpak install flathub com.sweethome3d.Sweethome3d org.blender.Blender`. | Ask the setup adult. |
| **Dock gone** | Restart the device once. | If still gone, tell the setup adult. |
| **No Wi-Fi** | `nmcli device status`. The Wi-Fi line should say `connected`. | `sudo nmcli device wifi connect "<SSID>" password "<password>"` |
| **Backup ✗** (no new files in Backup) | Check Wi-Fi. Check the newest date in the Tresorit app. | Fix Wi-Fi first. Then tell the setup adult. See [5-backup-and-share.md](5-backup-and-share.md) to configure `kiosk/60-backup.sh`. |
| **Library empty** | `ls /home/$KID/Library` | Check Wi-Fi with `ping -c 2 fedoraproject.org`. Run `sudo bash library/build-library.sh` again. Read the errors first. |
| **Disk full** | `df -h /` | Do not delete art yet. Ask the setup adult first. A delete can sync to the backup. |
| **Forgot passwords** | `$ADMIN` has no password login. Use Tailscale SSH. | Root: run `sudo passwd root` as `$ADMIN`. Forgot the GRUB password or the device is locked: reinstall with [2-install-fedora.md](2-install-fedora.md), then restore from the backup. |
| **Kid found a way out** | Ask what they did. Run `sudo nft list ruleset`. | Do not blame the kid. Tell the setup adult. Re-run the tests in [3-run-the-kit.md](3-run-the-kit.md), section 6. |

## Restart the device

1. Tell the kid to save. Krita closes at restart.
2. Run `sudo systemctl reboot`. Or press the power button.

## If nothing works

1. Write down the problem and the time.
2. Use Tailscale SSH to check the device: `ssh $ADMIN@$HOST`.
3. Do not change `/etc/grub.d/`.
