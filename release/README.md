# Desktop release (maintainers)

The try-it downloads for Windows, Mac, and Linux. The kiosk does not use these files.

| File | Use |
|---|---|
| `apps.toml` | Pinned upstream builds (Krita, Blender, Sweet Home 3D) and app sources, each with its SHA-256 |
| `requirements.txt` | Python packages for the build (pinned) |
| `build.py` | `fetch` (download, check SHA-256), `app` (PyInstaller), `pack` (installer, DMG, or tar.gz + SHA256SUMS), `sources` |
| `art-kit.spec` | PyInstaller spec: `app/desktop.py` + `app/library.py` + `app/ui` + `lessons/` + `library/*.txt` |
| `art-kit.iss` | Windows installer (Inno Setup): `Program Files\Art Kit`, Start menu entries, one uninstaller |
| `install.sh` | Linux: user install in `~/.local/opt/art-kit` (unpacks the AppImages: no FUSE needed), menu entries, then the books download (no root) |
| `icon.png` | App icon |
| `../.github/workflows/release.yml` | CI: builds all four, smoke test (`--selftest`), uploads to the GitHub Release |

## Make a release

1. Change `app/VERSION` (for example `0.2.0`). Commit.
2. Tag and push: `git tag v0.2.0 && git push origin v0.2.0`. CI checks that the tag matches `app/VERSION`.
3. CI builds and uploads `ArtKit-Setup-x.y.z.exe`, `ArtKit-x.y.z-arm64.dmg`, `ArtKit-x.y.z-x64.dmg`, `ArtKit-x.y.z-x86_64.tar.gz`, the app sources, and `SHA256SUMS`.
4. A test run without a tag: Actions → Release → Run workflow. It makes a draft release.

The apps check `releases/latest` once a day and show "Version x.y.z is ready" (setting: "Check for updates").

## Update an upstream app

1. Download the new file. Run `sha256sum <file>`.
2. Change its `url` and `sha256` in `apps.toml`. Also change the matching `[source]` entry.
3. Change the version in `../THIRD-PARTY.md`.
4. If the folder or program name changes, change `APPS` in `app/desktop.py` and the paths in `art-kit.iss` and `install.sh`.

## Build on your computer

```sh
python3 -m venv /tmp/venv && /tmp/venv/bin/pip install -r release/requirements.txt
/tmp/venv/bin/python release/build.py fetch && /tmp/venv/bin/python release/build.py app
build/pyi/artkit/artkit --selftest           # Linux (Mac: "build/pyi/Art Kit.app/Contents/MacOS/Art Kit")
/tmp/venv/bin/python release/build.py pack   # dist/
```

Downloads go to `release/cache/` (they resume). Run the app from the source: `python3 app/desktop.py` (needs `pywebview`, `pypdfium2`, `pillow`, `markdown`).

## How the app works

- `app/desktop.py` serves `library.handle()` on `127.0.0.1` (random port). Every request needs a random token (a cookie from the first URL) and the right `Host`.
- Data: `~/Art Kit/` (`Art/`, `Art/Notes/`, `Library/`). The lessons ship in the app; the first start copies them and builds the search index.
- Books and pictures: the app runs `library/build_library.py` (the kiosk builder) at each start until all is there (about 3 GB). The first start shows a progress screen. Linux `install.sh` runs it in the terminal (`ArtKit/AppRun --get-library`).
- Kit settings, only when no config exists: Krita defaults (`kritarc`), Blender preferences (no splash, Emulate 3 Button Mouse), Sweet Home 3D Java options.
- Env for tests: `ART_KIT_APPS=<dir>` (the bundled apps), `ART_KIT_UPDATE_URL=<url>` (a fake release JSON), `ART_KIT_KIOSK=1` (no update check).
- Signing: none. Windows SmartScreen and macOS Gatekeeper show one warning. Krita, Blender, and Sweet Home 3D keep their own signatures.
