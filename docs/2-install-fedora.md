# 2. Install Fedora

For the setup adult. Do this after [1-get-a-device.md](1-get-a-device.md). Time: about 1 hour.

Install Fedora on the device. Then run the kit ([3-run-the-kit.md](3-run-the-kit.md)).

## 1. Choose the download

Use **Fedora 45 or newer** (the dock needs gnome-kiosk 51). Use the **Everything netinstall** image. In the installer, choose **Minimal Install**.

| Option | Pick it when |
|---|---|
| **Everything netinstall + Minimal Install** (use this) | The kit installs only what it needs. No desktop is left to remove. The installer downloads packages, so Wi-Fi must work. |
| Workstation Live | You want a graphical installer and do not mind extra apps. The kit still works, but the device keeps more software. |

1. Go to fedoraproject.org. Choose **Download**. Choose the **Everything** netinstall image for x86_64.
2. Keep the file. It is an ISO file.

## 2. Make the USB stick

You need a USB stick of 8 GB or more. Writing erases the stick.

| # | Step |
|---|---|
| 1 | On your computer, install **Fedora Media Writer** from getfedora.org. |
| 2 | Open Fedora Media Writer. Select the ISO file from step 1 of section 1. |
| 3 | Select your USB stick. Write the image. Wait for it to finish. |

**You should see:** Media Writer reports that the write is complete.

## 3. Boot from the USB stick

1. Plug the USB stick into the device.
2. Turn the device off.
3. Turn it on. Press the boot menu key for your device.

| Device | Boot menu key |
|---|---|
| Surface | Hold **Volume Down**. Press **Power**. Keep holding Volume Down until the menu shows. |
| Lenovo | **F12** at power on |
| HP | **F9** at power on |
| Other | Try **Esc**, **F12**, **F9**, or **F8** at power on. Check the device manual. |

**You should see:** the Fedora boot menu. Choose the line that starts with **Install Fedora**.

## 4. Use the installer

Follow the installer in this order.

| Screen | Choose |
|---|---|
| Language, keyboard | Your language and keyboard |
| Network & Host Name | Connect to Wi-Fi. Wait until it shows connected. |
| Software Selection | **Minimal Install** |
| Installation Destination | Whole disk (see disk layout below) |
| User Creation | Only `$ADMIN` (see user table below) |
| Root Account | Skip. You set the root password later. |

### Disk layout

| Setting | Choose |
|---|---|
| Disk | The whole disk. This erases all data on it. |
| Storage configuration | Automatic |
| File system | btrfs (the default) |
| Disk encryption | Off. This kit does not use disk encryption. |

### Users

| User | Create at install? | Make administrator? |
|---|---|---|
| `$ADMIN` | Yes | Yes. Tick **Make this user administrator**. |
| `$KID` | No. `install.sh` creates it. | Never. |

Use the same name for `$ADMIN` that you set in `kit.conf` later.

## 5. Finish the install

1. Click **Begin Installation**. Wait until it finishes.
2. Remove the USB stick.
3. Restart the device.

**You should see:** a text login prompt. Log in as `$ADMIN`.

## 6. Secure Boot

| Device | Secure Boot during install | After install |
|---|---|---|
| Surface | Off | Turn on after the MOK step in [3-run-the-kit.md](3-run-the-kit.md), section 5, step c. |
| Other | Leave on or off. Both work. | Nothing to do. |

Surface MOK note: the blue **MokManager** screen appears after the first reboot that follows `install.sh`. Choose **Enroll MOK**, then **Continue**, then **Yes**. Type the password `surface` (QWERTY layout).

## 7. First update

Log in as `$ADMIN`. Run:

```sh
sudo dnf upgrade --refresh -y
sudo reboot
```

**You should see:** `Complete!` at the end of the upgrade. The device restarts.

## Checklist

- [ ] Fedora installed with Minimal Install.
- [ ] Only `$ADMIN` exists. `$ADMIN` is an administrator.
- [ ] Wi-Fi works.
- [ ] First update done.
- [ ] Next: [3-run-the-kit.md](3-run-the-kit.md).
