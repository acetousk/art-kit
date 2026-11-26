#!/bin/sh
# Run as root on the kiosk device. Reads kiosk settings and checks kid restrictions.
set -u
. "$(dirname "$0")/../kit.conf"
failed=0
check() {
  label=$1; shift
  if "$@"; then printf 'PASS %s\n' "$label"; else printf 'FAIL %s\n' "$label"; failed=1; fi
}
check 'GDM autologin user' grep -q "^AutomaticLogin=$KID$" /etc/gdm/custom.conf
check 'Kiosk session assigned' grep -q '^Session=krita-kiosk$' "/var/lib/AccountsService/users/$KID"
check 'Kid firewall rule loaded' sh -c "nft list ruleset | grep -Eq 'skuid (\"?$KID\"?|$(id -u "$KID")) drop'"
check 'Kid has no network (the admin has)' sh -c "runuser -u '$ADMIN' -- curl -fsSI -m 8 https://fedoraproject.org >/dev/null &&
  ! runuser -u '$KID' -- curl -fsSI -m 8 https://fedoraproject.org >/dev/null 2>&1"
check 'USB storage blocked' sh -c "grep -q 'install usb-storage /bin/false' /etc/modprobe.d/kiosk-usb.conf && grep -q 'install uas /bin/false' /etc/modprobe.d/kiosk-usb.conf"
check 'Krita Python removed' sh -c "! find /usr -name kritapykrita.so -print -quit 2>/dev/null | grep -q ."
for app in com.sweethome3d.Sweethome3d org.blender.Blender; do
  if flatpak override --show "$app" 2>/dev/null | grep -q 'shared=!network;' &&
     flatpak override --show "$app" 2>/dev/null | grep -q "/home/$KID/Art" &&
     flatpak override --show "$app" 2>/dev/null | grep -Eq "^filesystems=(.*;)?/var/lib/art-kit/Library:ro(;|$)"; then
    printf 'PASS Flatpak overrides: %s\n' "$app"
  else printf 'FAIL Flatpak overrides: %s\n' "$app"; failed=1; fi
done
check 'Blender on X11 (dock can raise it)' sh -c "flatpak override --show org.blender.Blender | grep -q '!wayland'"
check 'MIME cache (Krita save dialog)' test -s /usr/share/mime/mime.cache
check 'Krita 2 GB defaults' grep -q '^AutoSaveInterval=300$' /etc/xdg/kritarc
check 'Sweet Home 3D Java options' sh -c "flatpak override --show com.sweethome3d.Sweethome3d | grep -q 'Xmx700m'"
BV=$(LC_ALL=C flatpak info org.blender.Blender | awk '$1 == "Version:" { split($2, v, "."); print v[1] "." v[2] }')
check 'Blender preferences (no Quick Setup)' test -f "/home/$KID/.var/app/org.blender.Blender/config/blender/$BV/config/userpref.blend"
check 'zram and disk swap' sh -c "swapon --show=NAME --noheadings | grep -q zram && swapon --show=NAME --noheadings | grep -q /var/swapfile"
check 'Dock window rules' grep -q '^match-class=org.artkit.Dock$' /usr/local/share/gnome-kiosk/window-config.ini
check 'Dock running' systemctl --user -M "$KID@" -q is-active art-dock.service
check 'One app running' sh -c "[ \$(systemctl --user -M '$KID@' list-units --state=active --no-legend krita-kiosk.service art-library.service art-sweethome3d.service art-blender.service | wc -l) -eq 1 ]"
check 'Library outside the kid home' sh -c "[ \"\$(readlink /home/$KID/Library)\" = /var/lib/art-kit/Library ] && [ \"\$(stat -c %U /var/lib/art-kit/Library)\" = root ]"
check 'Library read-only for the kid' sh -c "! runuser -u '$KID' -- touch '/home/$KID/Library/.write-test' 2>/dev/null"
check 'Library readable for the kid' runuser -u "$KID" -- test -r "/home/$KID/Library/CREDITS.md"
exit "$failed"
