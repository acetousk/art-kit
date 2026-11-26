#!/bin/sh
# Art kiosk (GNOME Kiosk) on Fedora (Everything netinstall, "Minimal Install").
# Admin access for the setup adult: Tailscale + T3 Code. Settings: kit.conf. Run as root after the first boot. Reboot when done.
set -e

. "$(dirname "$0")/../kit.conf"   # KID, ADMIN, HOST, SURFACE

# 1. linux-surface kernel (Surface devices only): pen (iptsd), touch, Wi-Fi fixes.
if [ "$SURFACE" = yes ]; then
dnf config-manager addrepo --from-repofile=https://pkg.surfacelinux.com/fedora/linux-surface.repo
dnf install -y --allowerasing kernel-surface iptsd libwacom-surface kernel-surface-default-watchdog
dnf install -y surface-secureboot
systemctl enable linux-surface-default-watchdog.path
fi

# 2. GNOME Kiosk (Wayland, one app) + Krita. No desktop. Wi-Fi for updates and admin.
dnf install -y --setopt=install_weak_deps=False gnome-kiosk gdm gnome-session \
  xorg-x11-server-Xwayland iio-sensor-proxy krita NetworkManager-wifi linux-firmware nftables
systemctl set-default graphical.target
systemctl enable gdm
hostnamectl set-hostname "$HOST"

# 3. Kid user: no sudo, GDM autologin into the Krita kiosk session.
id "$KID" >/dev/null 2>&1 || useradd -m "$KID"
cat > /etc/gdm/custom.conf <<EOF
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=$KID
EOF
mkdir -p /var/lib/AccountsService/users
printf '[User]\nSession=krita-kiosk\nSystemAccount=false\n' > /var/lib/AccountsService/users/$KID

# 4. Session = GNOME Kiosk + Krita only. Root-owned files; the kid cannot edit them.
#    If Krita quits, systemd starts it again.
cat > /usr/share/wayland-sessions/krita-kiosk.desktop <<'EOF'
[Desktop Entry]
Name=Krita Kiosk
Exec=gnome-session --session krita-kiosk
TryExec=gnome-session
Type=Application
DesktopNames=GNOME-Kiosk;GNOME;
X-GDM-SessionRegisters=false
EOF
printf '[GNOME Session]\nName=Krita Kiosk\n' > /usr/share/gnome-session/sessions/krita-kiosk.session
mkdir -p /etc/systemd/user/gnome-session@krita-kiosk.target.d
cat > /etc/systemd/user/gnome-session@krita-kiosk.target.d/session.conf <<'EOF'
[Unit]
Requires=org.gnome.Kiosk.target
Requires=krita-kiosk.service
Wants=org.gnome.SettingsDaemon.A11ySettings.target
Wants=org.gnome.SettingsDaemon.MediaKeys.target
Wants=org.gnome.SettingsDaemon.Power.target
EOF
cat > /etc/systemd/user/krita-kiosk.service <<'EOF'
[Unit]
Description=Krita (kiosk)
BindsTo=gnome-session.target
After=gnome-session.target

[Service]
ExecStart=/usr/bin/krita --fullscreen
Restart=always
RestartSec=1
EOF

# 5. No VT switching, no SysRq, no extra consoles.
mkdir -p /etc/dconf/db/local.d/locks
: > /etc/dconf/db/local.d/00-kiosk
: > /etc/dconf/db/local.d/locks/00-kiosk
echo '[org/gnome/mutter/wayland/keybindings]' >> /etc/dconf/db/local.d/00-kiosk
for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  echo "switch-to-session-$n=['']" >> /etc/dconf/db/local.d/00-kiosk
  echo "/org/gnome/mutter/wayland/keybindings/switch-to-session-$n" >> /etc/dconf/db/local.d/locks/00-kiosk
done
grep -q '^system-db:local' /etc/dconf/profile/user 2>/dev/null || printf 'user-db:user\nsystem-db:local\n' > /etc/dconf/profile/user
dconf update
echo 'kernel.sysrq = 0' > /etc/sysctl.d/90-kiosk.conf
mkdir -p /etc/systemd/logind.conf.d
printf '[Login]\nNAutoVTs=0\nReserveVT=0\n' > /etc/systemd/logind.conf.d/kiosk.conf

# 6. Block USB storage (no outside files or plugins).
printf 'install usb-storage /bin/false\ninstall uas /bin/false\n' > /etc/modprobe.d/kiosk-usb.conf

# 7. Remove Krita's Python support (Scripter = shell escape). _netsharedpath keeps it out after upgrades.
PY_SO=$(rpm -qla 'krita*' | grep -E 'kritapykrita\.so$' | paste -sd:)
[ -n "$PY_SO" ] || { echo "ERROR: kritapykrita.so not found; check Krita's Python plugin by hand." >&2; exit 1; }
echo "%_netsharedpath $PY_SO" > /etc/rpm/macros.kiosk
echo "$PY_SO" | tr : '\n' | xargs rm -f

# 8. No network for the kid user. Root, Tailscale, and the admin keep network.
cat > /etc/nftables/kiosk.nft <<EOF
table inet kiosk {
  chain output {
    type filter hook output priority 0; policy accept;
    meta skuid "$KID" drop
  }
}
EOF
grep -q kiosk.nft /etc/sysconfig/nftables.conf || echo 'include "/etc/nftables/kiosk.nft"' >> /etc/sysconfig/nftables.conf
systemctl enable nftables

# 9. Admin user $ADMIN (sudo). No password login; access only over Tailscale SSH.
id "$ADMIN" >/dev/null 2>&1 || useradd -m -G wheel "$ADMIN"
passwd -l "$ADMIN"
echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/90-$ADMIN
chmod 440 /etc/sudoers.d/90-$ADMIN

# 10. Tailscale (remote access) and automatic updates (night reboot: see kiosk-maintenance-plan.md).
dnf config-manager addrepo --from-repofile=https://pkgs.tailscale.com/stable/fedora/tailscale.repo
dnf install -y tailscale dnf5-plugin-automatic
systemctl enable --now tailscaled
mkdir -p /etc/dnf
printf '[commands]\napply_updates = yes\nreboot = never\n' > /etc/dnf/automatic.conf
systemctl enable dnf5-automatic.timer

# 11. T3 Code for the admin user (never as root).
su - "$ADMIN" -c 'curl -fsSL https://t3.codes/install.sh | sh'

# 12. Library (read-only for the kid, about 3.2 GB). Needs library-inspiration.txt next to this script.
#     Tutorials/1-Graphic-Design: "Graphic Design and Print Production Fundamentals", ch. 1-3 by Alex Hass
#       (BCcampus 2015, CC BY 4.0), as page images.
#     Tutorials/2-Pepper-and-Carrot + 3-Brushes: David Revoy, www.peppercarrot.com (CC BY 4.0 / brushes CC0).
#     Inspiration: Art Institute of Chicago open access (CC0), 5 collections.
dnf install -y unzip poppler-utils
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
LIB=/home/$KID/Library
T=$LIB/Tutorials
mkdir -p "$T/1-Graphic-Design" "$T/2-Pepper-and-Carrot" "$T/3-Brushes" "$LIB/Inspiration"

GD=https://opentextbc.ca/graphicdesign/open/download?type=pdf
curl -fsSL -A "$UA" -o /tmp/gd.pdf "$GD"
pdftoppm -f 3 -l 3 -r 130 -png /tmp/gd.pdf "$T/1-Graphic-Design/000-license"      # credits + CC BY page
pdftoppm -f 17 -l 95 -r 130 -png /tmp/gd.pdf "$T/1-Graphic-Design/page"           # ch. 1-3
rm -f /tmp/gd.pdf

PC=https://www.peppercarrot.com/0_sources
for ep in $(curl -fsSL "$PC/" | grep -oE 'href="ep[0-9]+_[^"/]+/"' | sed 's/href="//;s/\/"//'); do
  curl -fsSL -o /tmp/art.zip "$PC/$ep/zip/${ep}_art-pack.zip" || { echo "skip $ep"; continue; }
  unzip -oq /tmp/art.zip -d "$T/2-Pepper-and-Carrot/$ep"
done
rm -f /tmp/art.zip
curl -fsSL -o /tmp/brushes.zip https://www.peppercarrot.com/extras/resources/deevad-bundle_25.01.zip
unzip -oq /tmp/brushes.zip -d "$T/3-Brushes" && rm -f /tmp/brushes.zip

grep -v '^#' "$(dirname "$0")/../library/inspiration.txt" | while IFS='|' read -r dir file url credit; do
  mkdir -p "$LIB/Inspiration/$dir"
  curl -fsSL -A "$UA" -o "$LIB/Inspiration/$dir/$file" "$url" || echo "skip $file"
  echo "$file: $credit" >> "$LIB/Inspiration/CREDITS.txt"
  sleep 1   # be polite to the museum server
done

chown -R root:root "$LIB"
chmod -R a+rX,go-w "$LIB"

echo "Done. Manual steps left: see the comment block at the end of this file."

# MANUAL STEPS (do these yourself):
# a. Root password: long, only you know it.  ->  passwd root
# b. GRUB password (blocks boot-entry edits; normal boot needs no password):  grub2-setpassword
#    Keep Fedora's hidden menu. Hold Shift or Esc at boot to pick the old kernel for rollback.
# c. Secure Boot: reboot, enroll the linux-surface MOK key (password: surface), then turn Secure Boot on.
# d. UEFI: leave unlocked (no password, USB boot stays on).
# e. Tailscale:  tailscale up --ssh   (open the printed link, sign in, then turn off key expiry
#    for this device in the Tailscale admin console).
# f. T3 Code:  sudo -iu $ADMIN t3 up   (open the printed sign-in link). Then add this machine in
#    T3 Code on your computer: Settings -> Environments -> Add environment -> SSH -> $ADMIN@$HOST.
#    Install and sign in to an agent for $ADMIN if you want agents to run here (e.g. claude auth login).
# g. Wi-Fi: nmcli device wifi connect "<SSID>" password "<password>"
# h. Test: pen pressure in Krita, Ctrl+Alt+F2 (must do nothing), quit Krita (must restart), Scripts menu (must be empty),
#    screen rotation, low-battery action,
#    sudo -u $KID curl -sI https://fedoraproject.org (must fail), tailscale ssh $ADMIN@$HOST (must work).
