#!/bin/sh
# Daily page for the family: /home/$KID/Art/Daily/<YYYY-MM-DD>.html (plain HTML, no JavaScript).
# It is in the Backup tresor, so parents see it in the Tresorit app.
# Install (root, once): sh kiosk/70-daily.sh   -> /usr/local/sbin/art-kit-daily + timer at 21:00.
# Run by hand: systemctl start art-kit-daily.service
#
# Inputs:
#   Files saved today:  files in ~/Art changed today, grouped by folder (Topic/NNN lesson).
#   Lessons done today: ~/Art/.library-log, written by the Library app. One line per lesson marked done:
#                         <ISO time, local><TAB><Topic>/<NNN> <Title>
#   Time in each app:   the kid's systemd user manager journal: "Started <unit>" to its first end event
#                       (Stopped, Failed, Deactivated, or Consumed), cut to today. Units still running count until now.
#                       Units: krita-kiosk, art-library (install.sh), art-sweethome3d, art-blender (the dock).
set -eu

if [ "${1:-}" != run ]; then
  . "$(dirname "$0")/../kit.conf"   # KID
  install -m 755 "$0" /usr/local/sbin/art-kit-daily
  cat > /etc/systemd/system/art-kit-daily.service <<EOF
[Unit]
Description=Daily art page for the family

[Service]
Type=oneshot
User=$KID
Environment=KID=$KID
ExecStart=/usr/local/sbin/art-kit-daily run
EOF
  cat > /etc/systemd/system/art-kit-daily.timer <<'EOF'
[Unit]
Description=Write the daily art page at 21:00

[Timer]
OnCalendar=*-*-* 21:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
  systemctl daemon-reload
  systemctl enable --now art-kit-daily.timer
  echo "Done. Test now: systemctl start art-kit-daily.service"
  exit 0
fi

# Run mode (as the kid: the page is in her Art folder, so root never writes there). KIDHOME and DAILY_JOURNAL (a file of journal lines) are for tests only.
KID=${KID:?set KID}
ART=${KIDHOME:-/home/$KID}/Art
OUT=$ART/Daily
DAY=$(date +%F)
LOG=$ART/.library-log

esc() { sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

journal() {
  if [ -n "${DAILY_JOURNAL:-}" ]; then cat "$DAILY_JOURNAL"; return; fi
  U=$(id -u "$KID")
  # 39f5...: unit started. End events: 9d1a... stopped, d9b3... failed, 7ad2... deactivated, ae8f... resources.
  # Since yesterday: an app open at midnight started then (awk counts only the time after midnight).
  journalctl -q --no-pager -o short-unix --since yesterday \
    _UID="$U" MESSAGE_ID=39f53479d3a045ac8e11786248231fbf + _UID="$U" MESSAGE_ID=9d1aaa27d60140bd96365438aad20286 \
    + _UID="$U" MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c + _UID="$U" MESSAGE_ID=7ad2d189f7e94e70a38c781354912448 \
    + _UID="$U" MESSAGE_ID=ae8f7b866b0347b9af31fe1c80b127c0
}
# Units running now. A start with no end counts until now only if the unit runs (not after a power cut). DAILY_LIVE is for tests.
live() { echo " ${DAILY_LIVE-$(XDG_RUNTIME_DIR=/run/user/$(id -u "$KID") systemctl --user list-units --state=active --no-legend --plain 2>/dev/null | awk '{ printf "%s ", $1 }')} "; }

install -d -m 755 "$OUT"
{
  echo '<!DOCTYPE html>'
  echo '<html lang="en"><head><meta charset="utf-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1">'
  echo "<title>Art $DAY</title>"
  echo '<style>body{font-family:sans-serif;font-size:18px;line-height:1.4;margin:16px;max-width:40em}h2{margin-top:1.5em}</style>'
  echo '</head><body>'
  echo "<h1>Art: $DAY</h1>"

  echo '<h2>Lessons done today</h2><ul>'
  [ -f "$LOG" ] && awk -F '\t' -v d="$DAY" 'index($1, d) == 1 && $2 != "" { print $2 }' "$LOG" | sort -u | esc | sed 's|.*|<li>&</li>|'
  echo '</ul>'

  echo '<h2>Files saved today</h2>'
  find "$ART" \( -path "$OUT" -o -name '.*' \) -prune -o -type f -newermt "$DAY" -printf '%P\n' | sort | esc |
    awk '{ d = $0; f = $0; if (sub(/\/[^\/]*$/, "", d)) sub(/.*\//, "", f); else d = "(Art)"
           if (d != last) { if (last != "") print "</ul>"; print "<h3>" d "</h3><ul>"; last = d }
           print "<li>" f "</li>" }
         END { if (last != "") print "</ul>"; else print "<p>None.</p>" }'

  echo '<h2>Time in each app</h2><ul>'
  journal | awk -v now="$(date +%s)" -v live="$(live)" -v mid="$(date -d "$DAY" +%s)" '
    function app(u) { u = tolower(u); if (u ~ /^art-(blender|sweethome3d)/) return ""   # flatpak: only the app scope counts (not also the art-* unit)
      if (u ~ /^krita/) return "Krita"; if (u ~ /sweethome3d/) return "Sweet Home 3D"
      if (u ~ /blender/) return "Blender"; if (u ~ /library/) return "Library"; return "" }
    { u = $4 ~ /^(Started|Stopped)$/ ? $5 : $4; sub(/[.:]$/, "", u) }
    $4 == "Started" { if (app(u) != "") s[u] = $1 < mid ? mid : $1; next }
    u in s { if ($1 > s[u]) t[app(u)] += $1 - s[u]; delete s[u] }   # the first end event closes the session
    END { for (u in s) if (index(live, " " u " ")) t[app(u)] += now - s[u]
          for (a in t) printf "<li>%s: %d h %02d min</li>\n", a, t[a] / 3600, t[a] % 3600 / 60 }' | sort
  echo '</ul>'
  echo '</body></html>'
} > "$OUT/$DAY.tmp"
chmod 644 "$OUT/$DAY.tmp"
mv -f "$OUT/$DAY.tmp" "$OUT/$DAY.html"
