# Third-party software in the Art Kit desktop downloads

The desktop downloads (Windows, Mac, Linux) hold three free apps, unchanged, as their teams build them.
Each GitHub Release also has the exact source archive of each app version (files `krita-*.tar.xz`, `blender-*.tar.xz`, `SweetHome3D-*-src.zip`).
The pinned files and their SHA-256 are in [release/apps.toml](release/apps.toml).

## The apps

| App | Version | License | Builds | Source |
|---|---|---|---|---|
| Krita | 6.0.5 (all) | GNU GPL 3.0 or later | <https://download.kde.org/stable/krita/6.0.5/> | `krita-6.0.5.tar.xz` (same folder) |
| Blender | 5.3.0 (Windows, Mac Apple Silicon, Linux); 4.5.17 LTS (Mac Intel: Blender 5 has no Intel build) | GNU GPL 3.0 or later (code: GPL 2.0 or later) | <https://www.blender.org/download/> (mirror: ftp.nluug.nl) | `blender-5.3.0.tar.xz`, `blender-4.5.17.tar.xz` from <https://download.blender.org/source/> |
| Sweet Home 3D | 7.6.1 (Windows, Mac); 7.5 (Linux: 7.6.1 has no Linux build) | GNU GPL 2.0 or later | <https://sourceforge.net/projects/sweethome3d/files/SweetHome3D/> | `SweetHome3D-7.6.1-src.zip`, `SweetHome3D-7.5-src.zip` from <https://sourceforge.net/projects/sweethome3d/files/SweetHome3D-source/> |

Each app also contains other free libraries, with their license files in the app folder:
- Krita: Qt (LGPL 3.0) and others. See `share/krita/` (Linux), `Krita/` (Windows), or `krita.app/Contents/Resources` (Mac), and <https://invent.kde.org/graphics/krita>.
- Blender: see the `license` folder in the Blender folder, or <https://www.blender.org/about/license/>.
- Sweet Home 3D: a Java runtime (OpenJDK, GPL 2.0 with the Classpath Exception; source: <https://openjdk.org>), Java 3D, and others. See the `THIRDPARTY-LICENSE-*.TXT` files in the Sweet Home 3D folder.

## The Art Kit app

The Art Kit app (`app/desktop.py`, the Library app) is built with PyInstaller. It contains:

| Part | License | Source |
|---|---|---|
| Python | PSF License | <https://www.python.org> |
| pywebview | BSD 3-Clause | <https://github.com/r0x0r/pywebview> |
| pypdfium2 and PDFium | Apache 2.0 or BSD 3-Clause; PDFium: BSD 3-Clause | <https://github.com/pypdfium2-team/pypdfium2> |
| Pillow | MIT-CMU | <https://github.com/python-pillow/Pillow> |
| Python-Markdown | BSD 3-Clause | <https://github.com/Python-Markdown/markdown> |
| PySide6 and Qt WebEngine (Linux only) | LGPL 3.0 (Qt WebEngine: LGPL 3.0, Chromium parts: BSD and others) | <https://code.qt.io> |
| QtPy (Linux only) | MIT | <https://github.com/spyder-ide/qtpy> |
| pythonnet (Windows only) | MIT | <https://github.com/pythonnet/pythonnet> |
| PyObjC (Mac only) | MIT | <https://github.com/ronaldoussoren/pyobjc> |
| PyInstaller bootloader | GPL 2.0 with the bootloader exception | <https://github.com/pyinstaller/pyinstaller> |

The exact versions are in [release/requirements.txt](release/requirements.txt).
The lessons, books, and pictures have their own sources and licenses: see `CREDITS.md` in the Library.
