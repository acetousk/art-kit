#!/bin/bash
# Build the kid's read-only Library. Run as root on the device: sudo bash library/build-library.sh
# Safe to run again: it skips files that exist and resumes cut downloads.
# Env: LIB_ROOT=<dir> (default /home/$KID/Library)  CACHE=<dir> (default /var/cache/art-kit)
#      DRY=1 (print actions only)  ONLY=<regex> (use only list lines that match, for tests)
#      BLENDER_SRC=<dir> (Blender manual source, default /tmp/books/blender-manual)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(dirname "$HERE")"
# shellcheck source=/dev/null
. "$KIT/kit.conf"
LIB_ROOT="${LIB_ROOT:-/home/$KID/Library}"
CACHE="${CACHE:-/var/cache/art-kit}"
DRY="${DRY:-}"
ONLY="${ONLY:-.}"
BLENDER_SRC="${BLENDER_SRC:-/tmp/books/blender-manual}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
TODO=()

run() { if [ -n "$DRY" ]; then echo "+ $*"; else "$@"; fi; }
# list FILE: print the data lines that match ONLY.
list() { grep -v '^#' "$1" | grep -v '^[[:space:]]*$' | grep -E -- "$ONLY"; }
# get URL FILE: download once into FILE. Resume a cut download from FILE.part.
get() {
  [ -s "$2" ] && return 0
  if [ -n "$DRY" ]; then echo "+ curl $1 -> $2"; return 0; fi
  mkdir -p "$(dirname "$2")"
  curl -fL -A "$UA" --retry 3 -sS -C - -o "$2.part" "$1" && mv "$2.part" "$2"
}
# save URL DIR: an offline copy of one web page and its images.
# Same host only (no fonts or video players). .done marks a full copy.
save() {
  [ -e "$2/.done" ] && return 0
  run wget -q -e robots=off -U "$UA" -p -k -E -nd -P "$2" "$1" && run touch "$2/.done"
}

run mkdir -p "$LIB_ROOT" "$CACHE"

# 0. Check every book URL (HTTP 200 after redirects).
echo "== URL check (books.txt)"
if [ -n "$DRY" ]; then
  echo "skip URL checks in dry run"
else
  list "$HERE/books.txt" | while IFS='|' read -r _ name url _; do
    code=$(curl -sIL -A "$UA" -o /dev/null -w '%{http_code}' "$url")
    echo "$code $name"
  done
fi

# 1. Books/<name>/page-NNN.png + page-NNN.txt (NNN = PDF page number).
while IFS='|' read -r _ name url pages remove _; do
  pdf="$CACHE/$name.pdf"; out="$LIB_ROOT/Books/$name"
  get "$url" "$pdf" || { echo "skip $name (download failed)"; TODO+=("book $name"); continue; }
  run mkdir -p "$out"
  if [ -n "$DRY" ]; then echo "+ render $name pages=$pages remove=[$remove]"; continue; fi
  last=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
  first=1
  [ "$pages" != all ] && { first=${pages%-*}; last=${pages#*-}; }
  for ((p = first; p <= last; p++)); do
    case " $remove " in *" $p "*) continue ;; esac
    n=$(printf '%03d' "$p")
    [ -s "$out/page-$n.png" ] || pdftoppm -f "$p" -l "$p" -r 120 -png -singlefile "$pdf" "$out/page-$n"
    [ -e "$out/page-$n.txt" ] || pdftotext -f "$p" -l "$p" -layout "$pdf" "$out/page-$n.txt"
  done
  for p in $remove; do rm -f "$out/page-$(printf '%03d' "$p")".*; done   # removed pages never stay
done < <(list "$HERE/books.txt")

# 2. Manuals.
get https://docs.krita.org/en/epub/KritaManual.epub "$CACHE/KritaManual.epub" &&
  { [ -e "$LIB_ROOT/Krita-Manual/index.xhtml" ] || run unzip -oq "$CACHE/KritaManual.epub" -d "$LIB_ROOT/Krita-Manual"; }
save https://www.sweethome3d.com/users-guide/ "$LIB_ROOT/SweetHome3D-Guide"
if [ -d "$BLENDER_SRC/manual/grease_pencil" ]; then
  run mkdir -p "$LIB_ROOT/Blender-Manual"
  run cp -rT "$BLENDER_SRC/manual/grease_pencil" "$LIB_ROOT/Blender-Manual/Grease-Pencil"
  run cp "$BLENDER_SRC/LICENSE" "$LIB_ROOT/Blender-Manual/LICENSE.txt"
else
  echo "TODO: Blender Manual (Grease Pencil) not found in $BLENDER_SRC"; TODO+=("Blender Manual")
fi

# 3. Inspiration/<collection>/<file> + Inspiration/CREDITS.txt
run mkdir -p "$LIB_ROOT/Inspiration"
list "$HERE/inspiration.txt" | while IFS='|' read -r dir file url _; do
  get "$url" "$LIB_ROOT/Inspiration/$dir/$file" || echo "skip $file"
done
# Same columns as inspiration.txt (folder|file|url|credit): make-index.py reads this file.
[ -n "$DRY" ] || list "$HERE/inspiration.txt" > "$LIB_ROOT/Inspiration/CREDITS.txt"

# 4. Painting: Pepper&Carrot .kra sources (David Revoy, CC BY 4.0) and his brush bundle (CC0).
PC="$LIB_ROOT/Painting/Pepper-and-Carrot"
list "$HERE/revoy.txt" | while IFS='|' read -r ep url _; do
  get "$url" "$CACHE/$ep.zip" || { echo "skip $ep"; continue; }
  run mkdir -p "$PC/$ep"
  ls "$PC/$ep"/*.kra >/dev/null 2>&1 || run unzip -oq "$CACHE/$ep.zip" -d "$PC/$ep"
done
BR=https://www.peppercarrot.com/extras/resources/deevad-bundle_25.01.zip   # from davidrevoy.com/article1060
run mkdir -p "$LIB_ROOT/Painting/Brushes"
get "$BR" "$CACHE/deevad-bundle_25.01.zip" &&
  { [ -n "$(ls -A "$LIB_ROOT/Painting/Brushes" 2>/dev/null)" ] || run unzip -oq "$CACHE/deevad-bundle_25.01.zip" -d "$LIB_ROOT/Painting/Brushes"; }

# 5. Revoy/<slug>/: offline copies of the pages in revoy-pages.txt (slug|url|title|license).
if [ -f "$HERE/revoy-pages.txt" ]; then
  list "$HERE/revoy-pages.txt" | while IFS='|' read -r name url _; do save "$url" "$LIB_ROOT/Revoy/$name"; done
else
  echo "TODO: library/revoy-pages.txt is missing"; TODO+=("Revoy pages")
fi

# 6. Tutorials/<Topic>/<lesson>/ = the lesson folders (no RULES/COURSE/REVIEW/INDEX files).
for topic in "$KIT/lessons"/*/; do
  t=$(basename "$topic")
  for lesson in "$topic"*/; do
    run mkdir -p "$LIB_ROOT/Tutorials/$t"
    run cp -r "${lesson%/}" "$LIB_ROOT/Tutorials/$t/"
  done
done
run find "$LIB_ROOT/Tutorials" \( -name RULES.md -o -name COURSE.md -o -name REVIEW.md -o -name INDEX.md \) -delete

# 7. CREDITS.md from all lists.
if [ -z "$DRY" ]; then
  {
    echo "# Credits"; echo
    echo "## Books (Books/<name>/)"; grep -v '^#' "$HERE/books.txt" | awk -F'|' 'NF{print "- "$2": "$6" <"$3">"}'; echo
    echo "## Manuals"
    echo "- Krita-Manual: Krita Manual, the Krita team, GNU FDL 1.3 <https://docs.krita.org/en/epub/KritaManual.epub>"
    echo "- SweetHome3D-Guide: Sweet Home 3D User's Guide, Space Mushrooms <https://www.sweethome3d.com/users-guide/>."
    echo "  The site footer says: \"© Copyright 2026 Space Mushrooms - All rights reserved\" (no open license for the guide text)."
    echo "- Blender-Manual/Grease-Pencil: Blender Manual, Blender Documentation Team, CC BY-SA 4.0 <https://docs.blender.org/manual/>"
    echo
    echo "## Painting"; grep -v '^#' "$HERE/revoy.txt" | awk -F'|' 'NF{print "- Pepper-and-Carrot/"$1": "$3}'
    echo "- Brushes: David Revoy, Krita brushes 2025-01 bundle, CC0 <https://www.davidrevoy.com/article1060/krita-brushes-2025-01-bundle>"
    [ -f "$HERE/revoy-pages.txt" ] && { echo; echo "## Revoy"; grep -v '^#' "$HERE/revoy-pages.txt" | awk -F'|' 'NF{print "- "$1": David Revoy, "$3", "$4" <"$2">"}'; }
    echo; echo "## Inspiration (Art Institute of Chicago open access, CC0)"
    grep -v '^#' "$HERE/inspiration.txt" | awk -F'|' 'NF{print "- "$1"/"$2": "$4}'
    echo; echo "## Tutorials"; echo "- Art Kit lessons. Each lesson names its sources in its README.md."
  } > "$LIB_ROOT/CREDITS.md"
fi

# 8. Search index. make-index.py takes the home dir that holds Library/.
if [ -f "$KIT/app/make-index.py" ]; then
  if [ "$(basename "$LIB_ROOT")" = Library ]; then run python3 "$KIT/app/make-index.py" --root "$(dirname "$LIB_ROOT")"
  else echo "skip index: make-index.py needs a folder named Library"; fi
fi

# 9. Owner and modes: root-owned, read-only for all. "From Family" belongs to 60-backup.sh.
if [ "$(id -u)" = 0 ]; then
  run find "$LIB_ROOT" -path "$LIB_ROOT/From Family" -prune -o -exec chown root:root {} +
fi
run find "$LIB_ROOT" -path "$LIB_ROOT/From Family" -prune -o -exec chmod a+rX,go-w {} +

echo "== Sizes"
[ -n "$DRY" ] || { du -sh "$LIB_ROOT"/*; du -sh "$LIB_ROOT"; }
[ ${#TODO[@]} -eq 0 ] || echo "TODO: ${TODO[*]}"
