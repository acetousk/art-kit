# 3. Run the kit

For the setup adult. Do this after [2-install-fedora.md](2-install-fedora.md). Log in as `$ADMIN` at the device.

You need: Wi-Fi that works, and the `$ADMIN` password.

## 1. Get the kit

Choose one option.

| Option | Commands |
|---|---|
| **A. Git** (use this) | `sudo dnf install -y git`<br>`git clone -b kit-v1 https://github.com/acetousk/art-kit.git`<br>`cd art-kit` |
| **B. ZIP** | Download the ZIP from the GitHub page. Then run `sudo dnf install -y unzip`, `unzip <file>.zip`, and `cd` into the new folder. |

**You should see:** a folder with `kit.conf`, `kiosk/`, and `docs/` in it.

## 2. Edit kit.conf

1. Run `sudo dnf install -y nano`.
2. Run `nano kit.conf`.
3. Set the four lines below.
4. Save: press **Ctrl+O**, then **Enter**. Exit: press **Ctrl+X**.

| Line | Set to | Example |
|---|---|---|
| `KID` | The kid's user name. Use a nickname, not a real name. | `kid` |
| `ADMIN` | Your user name from the install. Must match exactly. | `helper` |
| `HOST` | The device name on your Tailscale network | `art-kiosk` |
| `SURFACE` | `yes` for a Microsoft Surface. `no` for any other device. | `no` |

## 3. Check the internet

`install.sh` downloads packages and files. Check the connection first.

```sh
ping -c 2 fedoraproject.org
```

**You should see:** `2 packets received`. If not, connect Wi-Fi with the command in section 5, step g.

## 4. Run install.sh

```sh
cd art-kit
sudo sh kiosk/install.sh
```

Run it with `sh`. The file is not marked as a program.

This step takes a long time. The library download is about 3 GB.

**You should see:** `Done. Manual steps left: see the comment block at the end of this file.`

If the script stops with an error, read the last lines. Fix the cause. Then run the command again.

## 5. Manual steps

Do these steps in order. Do not skip one.

| Step | What to do | Command | You should see |
|---|---|---|---|
| **a** | Set the root password. Use a long password. Only you know it. | `sudo passwd root` | `all authentication tokens updated successfully` |
| **b** | Set the GRUB password. It blocks boot-menu edits. A normal boot needs no password. | `sudo grub2-setpassword` | A prompt for the password, twice |
| **c** | **Surface only.** Restart. At the blue MokManager screen: **Enroll MOK**, **Continue**, **Yes**, type `surface`, then restart. Then turn on Secure Boot in UEFI (hold **Volume Up** and press **Power**). Other devices: restart only. | `sudo reboot` | The kiosk starts after restart |
| **d** | Do nothing. Leave UEFI without a password. | — | — |
| **e** | Connect Tailscale. Open the link. Sign in. Then in the Tailscale admin console, turn off key expiry for this device. | `sudo tailscale up --ssh` | A sign-in link |
| **f** | Start T3 Code for `$ADMIN`. Open the link. On your computer, add the device in T3 Code: **Settings**, **Environments**, **Add environment**, **SSH**, `$ADMIN@$HOST`. | `sudo -iu $ADMIN t3 up` | A sign-in link |
| **g** | Connect Wi-Fi. Use this only if Wi-Fi is down. Replace `<SSID>` and `<password>`. Keep the quotes. | `sudo nmcli device wifi connect "<SSID>" password "<password>"` | `successfully activated` |

Step g is last in the list. Steps 1 to 4 need Wi-Fi first. Connect Wi-Fi before you run `install.sh`.

## 6. Test

Run these checks by hand. `kiosk/tests.sh` is not installed by `kiosk/install.sh`.

- [ ] **Pen pressure:** In Krita, draw a light line, then a hard line. The line gets thicker when you press harder.
- [ ] **Keys:** Press **Ctrl+Alt+F2**. Nothing happens.
- [ ] **Quit:** In Krita, choose **File**, then **Quit**. Krita starts again.
- [ ] **Python:** Open **Tools**, then **Scripts**. There is no Scripter entry.
- [ ] **Rotation:** Turn the screen. The screen turns.
- [ ] **Low battery:** Test what the device does at low battery.
- [ ] **Kid has no network:** Run `sudo -u $KID curl -sI https://fedoraproject.org`. You should see an error.
- [ ] **Admin SSH:** From your computer, run `tailscale ssh $ADMIN@$HOST`. You should log in with no password prompt.

## Checklist

- [ ] `kit.conf` is set.
- [ ] `install.sh` finished with `Done.`
- [ ] Steps a to g are done.
- [ ] Every test in section 6 passes.
- [ ] Next: [4-first-day.md](4-first-day.md).
