# 1. Get a device (and prove it works before you pay)

For the setup adult. Read this before you buy anything.

## What the kit needs
| Need | Minimum | Better | Why |
|---|---|---|---|
| CPU | x86-64 (Intel or AMD), 2016 or newer | Intel 7th gen or newer | Fedora and the apps are built for x86-64. ARM laptops (Snapdragon, Apple) do not work. |
| RAM | 4 GB | 8 GB | Krita and Sweet Home 3D run in 4 GB. Blender is slow in 4 GB. |
| Disk | 64 GB SSD | 128 GB+ SSD | The library is about 3 GB; her art grows. No spinning disks (slow, break when dropped). |
| Graphics | Intel HD 620 or newer | Intel Iris / AMD | Open drivers work with no setup. Avoid NVIDIA-only laptops. |
| Pen | **Pressure works in Linux** | Pressure + tilt + eraser | Drawing without pressure is like drawing with a marker only. This is the most important check. |
| Battery | Holds 2 h | 4 h+ | Old batteries are the most common hidden problem. |
| Screen | Touch + pen, 10"+ | 12"+, 1920×1080+ | Big enough for Krita's tools and the canvas. |
| Keyboard | Any | Attached (Type Cover, 2-in-1) | There is no on-screen keyboard. Names, sizes, and search need keys. |

## Device types
| Type | Example (used price) | Pen in Linux | Verdict |
|---|---|---|---|
| **Wacom-pen 2-in-1** | Lenovo ThinkPad X1 Yoga, X13 Yoga, L13 Yoga; HP EliteBook x360 ($150–300) | Very good. Wacom pens work with the normal Linux kernel. Pressure, tilt, and eraser work. | **Best choice.** Least setup, fewest surprises. |
| **Surface Pro 4–7** | Surface Pro 5 + Surface Pen ($120–200) | Good with the **linux-surface** kernel and `iptsd`. Third-party pens can flicker (iptsd issue #195). | **Good**, if the pen is a genuine Microsoft Surface Pen. One extra install step. |
| **Laptop + USB pen tablet** | Any old laptop + One by Wacom / Wacom Intuos S ($40–70 for the tablet) | Excellent. The kernel supports Wacom tablets. | **Cheapest.** The kid draws on the tablet and looks at the screen. Takes a week to get used to. |
| **Laptop + Huion/XP-Pen tablet** | ($30–60) | Usually works; some models need extra drivers | OK. Check the model online first. |
| **Laptop, no pen** | — | — | Not for drawing. Fine for Sweet Home 3D only. |
| **Chromebook** | — | Locked firmware; Linux install is hard or impossible | **No.** |
| **iPad / Android tablet** | — | No Linux | **No.** (They are good art devices, but this kit cannot lock them down.) |
| **ARM Windows laptop** (Snapdragon) | — | Fedora support is not ready | **No.** |
| **Apple Mac** (Intel or M-series) | — | Pen: none; Linux support is limited | **No.** |

### Pens: what to buy
| Device | Pen | Avoid |
|---|---|---|
| Surface | Genuine **Microsoft Surface Pen** (model 1776 or 1744/1745) | Cheap "Surface-compatible" pens: they often flicker in Linux |
| Wacom 2-in-1 | The pen for that model (Wacom AES or EMR). Check the laptop's spec sheet. | "Active stylus" pens with no model listed |
| USB tablet | Wacom One by Wacom or Intuos S | No-name tablets with no Linux reports |

## How to prove it works (before you pay)
Bring the **kit test USB stick** when you look at the device. It boots Fedora Live and opens a test page. It changes nothing on the device.

### Make the test USB (once, 20 min)
1. Download the **Fedora Workstation Live** image from fedoraproject.org.
2. Write it to a USB stick (8 GB+) with **Fedora Media Writer**.
3. Copy `tools/device-check.sh` and `tools/pen-test.html` from this kit to a second small USB stick (or a folder on your phone you can open on the device).

### At the seller (15 min)
| # | Test | How | Pass |
|---|---|---|---|
| 1 | Boots from USB | Hold the boot-menu key at power on (Surface: hold **Volume Down**; Lenovo: **F12**; HP: **F9**). Pick the USB. | Fedora desktop appears |
| 2 | Hardware report | Open Terminal. Run `bash device-check.sh` | Prints all ✅ (see below) |
| 3 | **Pen pressure** | Open `pen-test.html` in Firefox. Draw light, then hard. | Line gets thicker when you press harder. Pressure number goes from about 0.1 to 1.0. |
| 4 | Pen buttons, eraser | Press the side button; flip the pen | The page shows "button" and "eraser" |
| 5 | Pen accuracy | Touch each of the 5 targets on the page | The dot lands on each target |
| 6 | No flicker | Draw slow circles for 30 seconds | No breaks, no jumping lines |
| 7 | Touch | Pinch on the page | Page zooms |
| 8 | Wi-Fi | Join your phone's hotspot | Connects |
| 9 | Keyboard, touchpad | Type in the page's text box | All keys work |
| 10 | Screen | Look at a white page | No dead pixels, no lines, no pressure marks |
| 11 | Battery | In the report | Health 70 %+ |

> Surface note: Fedora Live uses the normal kernel. On a Surface, **touch and pen may not work on the Live USB** (they need the linux-surface kernel). For a Surface, check instead: the pen works in Windows (open Paint or Whiteboard, draw light and hard), the pen is genuine Microsoft, and the device-check report passes. Then check pen pressure again after step 10 of the install.

### What `device-check.sh` reports
| Line | Pass |
|---|---|
| CPU | x86_64, 4+ threads |
| RAM | 4 GB+ |
| Disk | SSD, 64 GB+, SMART health OK |
| Battery | health % = full charge ÷ design capacity; 70 %+ |
| Graphics | Intel or AMD, OpenGL 4.5+ |
| Pen | a "stylus" or "pen" device with pressure (ABS_PRESSURE) |
| Touch | a touchscreen device |
| Wi-Fi | a wireless card that Linux sees |
| Secure Boot | on or off (both are OK; note it for the install) |

### After you buy (first day, before the install)
- [ ] Charge to 100 %, then use it for 2 hours. Check the battery left.
- [ ] Run the device check again at home.
- [ ] If any test fails, return it now. Most sellers accept a return in 1–2 days.

## Example
Surface Pro 5 (4 GB, 128 GB) + new genuine Surface Pen 1776: $158. Pen pressure checked in Windows at pickup; linux-surface kernel installed; pen pressure checked in Krita after install.
