#!/bin/sh
# Build the kid's read-only Library: sudo bash library/build-library.sh
# The builder is build_library.py (one builder for the kiosk and the desktop app). Same env: LIB_ROOT, CACHE, DRY, ONLY, BLENDER_SRC.
exec python3 "$(dirname "$0")/build_library.py" "$@"
