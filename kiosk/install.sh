#!/bin/sh
# Art kiosk (GNOME Kiosk) on Fedora (Everything netinstall, "Minimal Install").
# Admin access for the setup adult: Tailscale + T3 Code. Settings: kit.conf. Run as root after the first boot. Reboot when done.
set -e

. "$(dirname "$0")/../kit.conf"   # KID, ADMIN, HOST, SURFACE

# 1. linux-surface kernel (Surface devices only): pen (iptsd), touch, Wi-Fi fixes.
if [ "$SURFACE" = yes ]; then
dnf config-manager addrepo --overwrite --from-repofile=https://pkg.surfacelinux.com/fedora/linux-surface.repo
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
passwd -l "$KID"
cat > /etc/gdm/custom.conf <<EOF
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=$KID
EOF
mkdir -p /var/lib/AccountsService/users
printf '[User]\nSession=krita-kiosk\nSystemAccount=false\n' > /var/lib/AccountsService/users/$KID

# 4. Session = GNOME Kiosk + Krita, the dock, and the Library app. Root-owned files; the kid cannot edit them.
#    Only one app runs at a time (less memory): the dock closes the open app before it starts the next one.
#    If an app crashes, systemd starts it again. If the kid quits it, the dock opens Krita.
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
Wants=art-dock.service
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
Environment=QT_QPA_PLATFORM=xcb
ExecStart=/opt/art-kit/dock/krita-open
Restart=on-failure
RestartSec=1
EOF
# Library app and dock (steps 12 and 14). All apps run on X11 (Xwayland): the dock raises them with xdotool.
cat > /etc/systemd/user/art-library.service <<'EOF'
[Unit]
Description=Library app (kiosk)
BindsTo=gnome-session.target
After=gnome-session.target

[Service]
Environment=GDK_BACKEND=x11
ExecStart=/usr/bin/python3 /opt/art-kit/app/library-app.py
Restart=on-failure
RestartSec=1
EOF
cat > /etc/systemd/user/art-dock.service <<'EOF'
[Unit]
Description=Dock (kiosk)
BindsTo=gnome-session.target
After=gnome-session.target

[Service]
ExecStart=/usr/bin/python3 /opt/art-kit/dock/kiosk-dock.py
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
echo '[org/gnome/desktop/wm/keybindings]' >> /etc/dconf/db/local.d/00-kiosk
for key in switch-applications switch-applications-backward close; do
  echo "$key=['']" >> /etc/dconf/db/local.d/00-kiosk
  echo "/org/gnome/desktop/wm/keybindings/$key" >> /etc/dconf/db/local.d/locks/00-kiosk
done
echo "[org/gnome/mutter]" >> /etc/dconf/db/local.d/00-kiosk
echo "overlay-key=''" >> /etc/dconf/db/local.d/00-kiosk
echo "/org/gnome/mutter/overlay-key" >> /etc/dconf/db/local.d/locks/00-kiosk
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
dnf config-manager addrepo --overwrite --from-repofile=https://pkgs.tailscale.com/stable/fedora/tailscale.repo
dnf install -y tailscale dnf5-plugin-automatic
systemctl enable --now tailscaled
mkdir -p /etc/dnf
printf '[commands]\napply_updates = yes\nreboot = never\n' > /etc/dnf/automatic.conf
systemctl enable dnf5-automatic.timer

# 11. T3 Code for the admin user (never as root).
su - "$ADMIN" -c 'curl -fsSL https://t3.codes/install.sh | sh'

# 12. Library (read-only for the kid) and the Library app. build-library.sh lists the sources and makes the search index.
dnf install -y python3-gobject gtk4 webkitgtk6.0 python3-markdown poppler-utils urw-base35-fonts unzip wget xdotool xprop wmctrl
bash "$(dirname "$0")/../library/build-library.sh" || echo "WARNING: build-library.sh failed. Run it again (it resumes)."
rm -rf /opt/art-kit/app && mkdir -p /opt/art-kit && cp -r "$(dirname "$0")/../app" /opt/art-kit/app

# 13. Offline 3D apps. Keep network and file access limited for the kid.
dnf install -y flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y --noninteractive flathub com.sweethome3d.Sweethome3d org.blender.Blender
for app in com.sweethome3d.Sweethome3d org.blender.Blender; do
  flatpak override --system "$app" --unshare=network --nofilesystem=host --nofilesystem=home \
    --filesystem=/home/$KID/Art --filesystem=/home/$KID/Library:ro
done
flatpak override --system org.blender.Blender --nosocket=wayland --socket=x11   # X11: the dock can raise it

# 14. Dock at the bottom edge: Krita, Sweet Home 3D, Blender, Library, battery, backup state.
#     The window rules need gnome-kiosk 51 or newer (Fedora 45+). MONITOR = the screen name, for example eDP-1.
install -D -m 755 "$(dirname "$0")/dock/kiosk-dock.py" /opt/art-kit/dock/kiosk-dock.py
install -D -m 755 "$(dirname "$0")/dock/krita-open" /opt/art-kit/dock/krita-open
MON=$(grep -l '^connected' /sys/class/drm/card*-*/status | head -n 1 | cut -d/ -f5 | cut -d- -f2-)
mkdir -p /usr/local/share/gnome-kiosk
sed "s/MONITOR/$MON/" "$(dirname "$0")/dock/window-config.ini" > /usr/local/share/gnome-kiosk/window-config.ini

# 15. Daily page for the family at 21:00. The backup (60-backup.sh) needs the Tresorit installer: manual step i.
sh "$(dirname "$0")/70-daily.sh"

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
# i. Backup: set TRESORIT_EMAIL in kit.conf. Download tresorit_installer.run (tresorit.com/download). Then as root:
#    sh kiosk/60-backup.sh /path/to/tresorit_installer.run   (type the Tresorit password when asked).
