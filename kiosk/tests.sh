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
check 'Kid has no network' sh -c "! timeout 8 runuser -u '$KID' -- curl -fsSI https://fedoraproject.org >/dev/null 2>&1"
check 'USB storage blocked' sh -c "grep -q 'install usb-storage /bin/false' /etc/modprobe.d/kiosk-usb.conf && grep -q 'install uas /bin/false' /etc/modprobe.d/kiosk-usb.conf"
check 'Krita Python removed' sh -c "! find /usr -name kritapykrita.so -print -quit 2>/dev/null | grep -q ."
for app in com.sweethome3d.Sweethome3d org.blender.Blender; do
  if flatpak override --show "$app" 2>/dev/null | grep -q 'shared=!network;' &&
     flatpak override --show "$app" 2>/dev/null | grep -q "/home/$KID/Art" &&
     flatpak override --show "$app" 2>/dev/null | grep -q "/home/$KID/Library"; then
    printf 'PASS Flatpak overrides: %s\n' "$app"
  else printf 'FAIL Flatpak overrides: %s\n' "$app"; failed=1; fi
done
check 'Blender on X11 (dock can raise it)' sh -c "flatpak override --show org.blender.Blender | grep -q '!wayland'"
check 'Dock window rules' grep -q '^match-class=org.artkit.Dock$' /usr/local/share/gnome-kiosk/window-config.ini
check 'Dock running' systemctl --user -M "$KID@" -q is-active art-dock.service
check 'One app running' sh -c "[ \$(systemctl --user -M '$KID@' list-units --state=active --no-legend krita-kiosk.service art-library.service art-sweethome3d.service art-blender.service | wc -l) -eq 1 ]"
check 'Library read-only for the kid' sh -c "! runuser -u '$KID' -- touch '/home/$KID/Library/.write-test' 2>/dev/null"
check 'Library readable for the kid' runuser -u "$KID" -- test -r "/home/$KID/Library/CREDITS.md"
exit "$failed"
