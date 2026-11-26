#!/bin/sh
# Install Art Kit for this user (no root): ./install.sh       Remove it: ./install.sh --remove
# Files go to ~/.local/opt/art-kit. Menu entries: Art Kit, Krita, Blender, Sweet Home 3D. Your files stay in ~/Art Kit.
# The AppImages are unpacked here, so they need no FUSE. Then it gets the books and pictures into ~/Art Kit/Library (about 3 GB), with progress.
set -e
cd "$(dirname "$0")"
SRC="$(pwd)"
DEST="${ART_KIT_DEST:-$HOME/.local/opt/art-kit}"
MENU="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
MARK=.art-kit-install  # only a folder with this file is an Art Kit install (remove and replace touch nothing else)
[ "$(id -u)" != 0 ] || { echo "Run this as your own user, not as root."; exit 1; }
if [ -e "$DEST" ] && [ ! -e "$DEST/$MARK" ] && [ -n "$(ls -A "$DEST")" ]; then
  echo "$DEST has other files and is not an Art Kit install. Nothing is changed."; exit 1
fi
if [ "$1" = --remove ]; then
  rm -rf "$DEST" "$MENU"/art-kit*.desktop
  echo "Art Kit is removed. Your files in ~/Art Kit stay."; exit 0
fi
NEW="$DEST.art-kit-new"
rm -rf "$NEW"
mkdir -p "$NEW" "$MENU"
echo "Copying Art Kit, Krita, Blender, and Sweet Home 3D to $DEST ..."
cp -r Blender SweetHome3D icon.png "$NEW/"
for a in ArtKit Krita; do  # unpack: no FUSE needed, and a fast start
  (cd "$NEW" && "$SRC/$a.AppImage" --appimage-extract >/dev/null && mv squashfs-root "$a")
done
touch "$NEW/$MARK"
rm -rf "$DEST" "$MENU"/art-kit*.desktop   # an older version goes only now, after the new one is complete
mv "$NEW" "$DEST"
entry() {  # file, name, command, icon
  printf '[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nIcon=%s\nTerminal=false\nCategories=Education;Graphics;\n' "$2" "$3" "$4" > "$MENU/$1.desktop"
}
ART="env \"ART_KIT_APPS=$DEST\" \"$DEST/ArtKit/AppRun\""
entry art-kit 'Art Kit' "$ART" "$DEST/icon.png"
entry art-kit-krita 'Krita (Art Kit)' "\"$DEST/Krita/AppRun\" %F" krita
entry art-kit-blender 'Blender (Art Kit)' "\"$DEST/Blender/blender\" %F" "$DEST/Blender/blender.svg"
entry art-kit-sweethome3d 'Sweet Home 3D (Art Kit)' \
  "env \"_JAVA_OPTIONS=-Xmx700m -XX:+UseSerialGC -Dsun.java2d.opengl=false\" \"$DEST/SweetHome3D/SweetHome3D\" %F" "$DEST/SweetHome3D/SweetHome3DIcon.png"
miss=; for l in libOpenGL.so.0 libEGL.so.1 libGL.so.1; do PATH="$PATH:/sbin:/usr/sbin" ldconfig -p 2>/dev/null | grep -q "$l" || miss="$miss $l"; done
[ -z "$miss" ] || { echo "Missing parts for Krita and Blender:$miss. Install them with:"  # minimal installs lack these
  echo "  Fedora: sudo dnf install libglvnd-opengl libglvnd-egl libglvnd-glx"
  echo "  Ubuntu: sudo apt install libopengl0 libegl1 libgl1"
  echo "  Arch:   sudo pacman -S libglvnd"; }
command -v update-desktop-database >/dev/null && update-desktop-database "$MENU" 2>/dev/null || true
echo "Art Kit is installed. Open it from the app menu, or run: $ART"
# The books and pictures (the same builder as the app uses). Ctrl+C is safe: Art Kit goes on at its next start.
ART_KIT_APPS="$DEST" "$DEST/ArtKit/AppRun" --get-library
