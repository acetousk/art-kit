# PyInstaller spec for the Art Kit desktop app (all platforms). Run by release/build.py.
# The bundle holds the kiosk's Library app (app/library.py, app/ui), the lessons, and the library lists.
import glob, os, sys

R = os.path.dirname(SPECPATH)  # the repo
VERSION = open(os.path.join(R, 'app', 'VERSION')).read().strip()
datas = [(f'{R}/app/ui', 'ui'), (f'{R}/app/books-map.json', '.'), (f'{R}/app/VERSION', '.'),
         (f'{R}/app/make-index.py', 'app'), (f'{R}/lessons', 'lessons')] + [(f, 'library') for f in glob.glob(f'{R}/library/*.txt')]
# Linux: the Qt web view (PySide6). qtpy loads it by name, so name the modules here.
qt = ['PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore', 'PySide6.QtWebChannel', 'PySide6.QtNetwork'] if sys.platform.startswith('linux') else []
a = Analysis([f'{R}/app/desktop.py'], pathex=[f'{R}/app', f'{R}/library'], datas=datas,
             hiddenimports=['markdown', 'pypdfium2', 'PIL.Image'] + qt, excludes=['gi', 'tkinter', 'PyQt5', 'PyQt6'])
pyz = PYZ(a.pure)
name = 'artkit' if sys.platform.startswith('linux') else 'Art Kit'
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name=name, console=False, icon=f'{R}/release/icon.png')
coll = COLLECT(exe, a.binaries, a.datas, name=name)
if sys.platform == 'darwin':
    app = BUNDLE(coll, name='Art Kit.app', icon=f'{R}/release/icon.png', bundle_identifier='org.artkit.ArtKit', version=VERSION,
                 info_plist={'NSHighResolutionCapable': True, 'LSMinimumSystemVersion': '13.0',
                             'NSAppTransportSecurity': {'NSAllowsLocalNetworking': True}})  # ATS: the UI is http://127.0.0.1
