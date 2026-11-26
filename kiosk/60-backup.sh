#!/bin/sh
# Tresorit backup. Run as root, after install.sh. Names come from kit.conf.
#   sh kiosk/60-backup.sh /path/to/tresorit_installer.run   (then type the Tresorit password, press Enter)
#   2FA: TOTP=123456 sh kiosk/60-backup.sh ...
# The password is read from stdin once. This script never writes it to a file.
# Tresorit keeps its own login secret in /home/$ADMIN (autologin).
#
# Sources (official Tresorit docs):
#   Install:  https://support.tresorit.com/hc/en-us/articles/216114157-Tresorit-for-Linux-FAQ
#             (download tresorit_installer.run from https://tresorit.com/download, run it as a normal user)
#   CLI:      https://support.tresorit.com/hc/en-us/articles/360009330614-Using-Tresorit-CLI-for-Linux
#             (tresorit-daemon, login --password-on-stdin [--totp], sync --start, transfers, X11 libs)
#   Filters:  https://support.tresorit.com/hc/en-us/articles/217103697-Exclude-specific-file-types-from-sync-advanced
#             (.tresorit/Filters/local.filter, "[Ignore] <path>")
#
# Result:
#   Backup      = /home/$KID (except Library: install.sh downloads it again) + /home/$KID/.kiosk-etc/etc.tar.gz.
#                 $ADMIN reads the kid home through ACLs (read only). Make parents Readers in the Tresorit app.
#   From Family = synced to /home/$ADMIN/From Family. Root copies only .png .jpg .jpeg .pdf .txt
#                 to /var/lib/art-kit/Library/From Family (root:$KID, mode 750/640: the kid reads, cannot write).
#                 It is outside the kid home (~/Library is a link to it), so root never writes through her paths.
#   /run/art-kit/backup-state = "ok|sync|fail <ISO-time> [reason]" for the dock (every 15 min). sync = transfers still listed.
set -eu
. "$(dirname "$0")/../kit.conf"   # KID, ADMIN, TRESORIT_EMAIL

[ -n "$TRESORIT_EMAIL" ] || { echo "TRESORIT_EMAIL is empty in kit.conf: no backup."; exit 0; }

TD=/home/$ADMIN/.local/share/tresorit
CLI=$TD/tresorit-cli

# 1. Packages. The CLI doc says Tresorit needs X11 libs; these are the Fedora names of its Ubuntu list.
dnf install -y acl rsync xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon-x11

# 2. Client (as $ADMIN, never as root: FAQ). TODO: check if the installer asks questions.
if [ ! -x "$CLI" ]; then
  [ -n "${1:-}" ] || { echo "ERROR: give the installer: sh $0 /path/to/tresorit_installer.run" >&2; exit 1; }
  runuser -u "$ADMIN" -- sh "$1"
fi

# 3. Helper: root runs it. No argument: copy From Family, write the backup state. "nightly": ACLs + /etc copy.
cat > /usr/local/sbin/art-kit-backup <<EOF
#!/bin/sh
set -u
H=/home/$KID
E=\$H/.kiosk-etc
if [ "\${1:-}" = nightly ]; then
  # \$ADMIN reads the kid home. Files saved with mode 600 get the ACL here (setfacl also fixes the mask).
  # As the kid: she can change only her own files, so a link she makes cannot point root at other files.
  cd /   # the kid's find must be able to enter its start folder
  runuser -u $KID -- find "\$H" -path "\$H/Library" -prune -o ! -type l -exec setfacl -m u:$ADMIN:rX {} + 2>/dev/null
  runuser -u $KID -- find "\$H" -path "\$H/Library" -prune -o -type d -exec setfacl -m d:u:$ADMIN:rX {} + 2>/dev/null
  # Only the kiosk config that install.sh and these scripts write. No keys, Wi-Fi, or password files.
  # The kid cannot read it. tar exit 1 = a file changed while read (OK). A missing file is skipped.
  C="etc/gdm/custom.conf etc/systemd/user etc/dconf/db/local.d etc/dconf/profile/user etc/sysctl.d/90-kiosk.conf
     etc/systemd/logind.conf.d/kiosk.conf etc/modprobe.d/kiosk-usb.conf etc/rpm/macros.kiosk etc/xdg/kritarc
     etc/nftables/kiosk.nft etc/sysconfig/nftables.conf etc/dnf/automatic.conf etc/fstab etc/systemd/system/tresorit.service
     etc/systemd/system/art-kit-backup.service etc/systemd/system/art-kit-backup.timer etc/systemd/system/art-kit-daily.service
     etc/systemd/system/art-kit-backup-nightly.service etc/systemd/system/art-kit-backup-nightly.timer etc/systemd/system/art-kit-daily.timer
     usr/local/share/gnome-kiosk/window-config.ini var/lib/AccountsService/users/$KID"
  rm -f "\$E" 2>/dev/null   # a link the kid made (a real folder stays)
  mkdir -m 750 "\$E" 2>/dev/null
  # Work inside the folder (cd holds it): a link or a rename by the kid cannot move root's writes.
  cd "\$E" && [ "\$(pwd -P)" = "\$E" ] && [ "\$(stat -c %u .)" = 0 ] || { echo "\$E: not root's folder" >&2; exit 1; }
  chgrp $ADMIN . && chmod 750 .
  if tar -C / --ignore-failed-read -czf etc.tmp \$C || [ \$? -eq 1 ]; then
    chgrp $ADMIN etc.tmp && chmod 640 etc.tmp && mv -f etc.tmp etc.tar.gz   # only a good copy replaces the last one
  else rm -f etc.tmp; exit 1; fi
  exit 0
fi
# From Family: only Library file types. Root-owned, the kid reads only.
F="/home/$ADMIN/From Family"
if [ -d "\$F" ]; then
  rsync -rt --delete --delete-excluded --prune-empty-dirs \\
    --exclude='.*' --include='*/' --include='*.[pP][nN][gG]' --include='*.[jJ][pP][gG]' \\
    --include='*.[jJ][pP][eE][gG]' --include='*.[pP][dD][fF]' --include='*.[tT][xX][tT]' --exclude='*' \\
    "\$F/" "/var/lib/art-kit/Library/From Family/"
  chown -R root:$KID "/var/lib/art-kit/Library/From Family" && chmod -R u=rwX,g=rX,o= "/var/lib/art-kit/Library/From Family"
fi
# State for the dock. TODO: also parse "transfers --porcelain" errors (columns are not documented).
R= T=
systemctl -q is-active tresorit.service || R="sync service stopped"
[ -n "\$R" ] || T=\$(runuser -u $ADMIN -- $CLI transfers --tresor Backup --porcelain 2>/dev/null) || R="tresorit-cli error"
[ -n "\$R" ] || [ -n "\$(find "\$E/etc.tar.gz" -mmin -2880 2>/dev/null)" ] || R="etc copy older than 2 days"
install -d -m 755 /run/art-kit
if [ -z "\$R" ] && [ -n "\$T" ]; then echo "sync \$(date -Is)"   # files still go up: not "Backed up" yet
elif [ -z "\$R" ]; then echo "ok \$(date -Is)"; else echo "fail \$(date -Is) \$R"; fi > /run/art-kit/backup-state.tmp
chmod 644 /run/art-kit/backup-state.tmp && mv -f /run/art-kit/backup-state.tmp /run/art-kit/backup-state
EOF
chmod 755 /usr/local/sbin/art-kit-backup

# 4. Sync folders. Backup must not upload the Library (3.2 GB; it also holds From Family).
# TODO: check on the device that Tresorit uses a .tresorit folder we make before "sync --start".
# ~/Library is only a link now; the filter is in case Tresorit follows links. Like .kiosk-etc: no kid link, work inside.
T=/home/$KID/.tresorit
if [ -L "$T" ]; then rm -f "$T"; fi
mkdir -p -m 700 "$T" && cd "$T" && [ "$(pwd -P)" = "$T" ] && [ "$(stat -c %U .)" != "$KID" ] || { echo "$T: the kid's folder" >&2; exit 1; }
install -d -o "$ADMIN" -m 700 Filters && printf '[Ignore] Library\n' > Filters/local.filter && chown "$ADMIN" . Filters/local.filter && cd /
install -d -o "$ADMIN" -m 700 "/home/$ADMIN/From Family"
install -d -o root -g "$KID" -m 750 "/var/lib/art-kit/Library/From Family"

# 5. systemd units. The CLI doc: start tresorit-daemon with no arguments from an init script.
# TODO: check that tresorit-daemon stays in the foreground (Type=simple). If it forks, use Type=forking.
cat > /etc/systemd/system/tresorit.service <<EOF
[Unit]
Description=Tresorit sync as $ADMIN (Backup, From Family)
Wants=network-online.target
After=network-online.target

[Service]
User=$ADMIN
ExecStart=$TD/tresorit-daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
cat > /etc/systemd/system/art-kit-backup.service <<'EOF'
[Unit]
Description=Copy From Family to the Library, write the backup state

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/art-kit-backup
EOF
cat > /etc/systemd/system/art-kit-backup.timer <<'EOF'
[Unit]
Description=Backup state and From Family, every 15 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/art-kit-backup-nightly.service <<'EOF'
[Unit]
Description=ACLs for the admin and /etc copy into the Backup tresor

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/art-kit-backup nightly
EOF
cat > /etc/systemd/system/art-kit-backup-nightly.timer <<'EOF'
[Unit]
Description=Nightly backup prep at 03:00

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
/usr/local/sbin/art-kit-backup nightly   # first ACLs and /etc copy (after the units: they are in it)
systemctl enable --now tresorit.service

# 6. Login. The password goes from stdin to the CLI through a pipe (printf is a shell builtin: not in ps).
[ -t 0 ] && { printf 'Tresorit password for %s: ' "$TRESORIT_EMAIL" >&2; stty -echo; }
IFS= read -r PW
[ -t 0 ] && { stty echo; echo >&2; }
printf '%s\n' "$PW" | runuser -u "$ADMIN" -- "$CLI" login --email "$TRESORIT_EMAIL" --password-on-stdin ${TOTP:+--totp "$TOTP"}
unset PW

# 7. Start sync. Tresorit remembers it after restart (CLI doc). Make both tresors in the web app first (docs/5).
runuser -u "$ADMIN" -- "$CLI" sync --start Backup --path "/home/$KID"
runuser -u "$ADMIN" -- "$CLI" sync --start "From Family" --path "/home/$ADMIN/From Family"

systemctl enable --now art-kit-backup.timer art-kit-backup-nightly.timer
echo "Done. Check: sudo -u $ADMIN $CLI tresors ; cat /run/art-kit/backup-state"
