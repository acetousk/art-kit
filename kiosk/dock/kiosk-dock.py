#!/usr/bin/env python3
"""Art Kit dock: one bar at the bottom of the screen (GNOME Kiosk places it: window-config.ini).
Buttons: Krita, Sweet Home 3D, Blender, Library. Right side: battery and backup state.
A tap starts the app if it does not run (as a systemd user unit: 70-daily.sh counts unit time), then raises it.
"""
import datetime, json, os, subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gdk, Gio, GLib, Gtk

HEIGHT = 80  # same as set-height in window-config.ini
STATE = '/run/art-kit/backup-state'
# Label, systemd user unit, X11 window class (a regex for xdotool), start command (None = a service from install.sh).
# All four apps run on X11 (Xwayland): GNOME Kiosk raises an X11 window when xdotool asks (_NET_ACTIVE_WINDOW).
APPS = [
    ('Krita', 'krita-kiosk.service', '^krita$', None),
    ('Sweet Home 3D', 'art-sweethome3d.service', 'sweethome3d', ['flatpak', 'run', 'com.sweethome3d.Sweethome3d']),
    ('Blender', 'art-blender.service', '^blender$', ['flatpak', 'run', 'org.blender.Blender']),
    ('Library', 'art-library.service', '^library-app', None),
]
# Flat, quiet bar. Running apps get a short warm line under the name; the app in front gets a light pill.
CSS = b"""
window, .dock { background: #1e1e20; border-top: 1px solid #2c2c30; }
button { min-height: 56px; min-width: 150px; margin: 12px 4px; padding: 0 16px; font-size: 19px; font-weight: 600;
         color: #a8a8ae; background: none; border: none; border-radius: 12px; box-shadow: none; }
button:active { background: #3a3a40; }
button.running { color: #e8e8ec; background-image: linear-gradient(#d9a441, #d9a441);
                 background-size: 28px 4px; background-position: 50% 88%; background-repeat: no-repeat; }
button.front { color: #ffffff; background-color: #34343a; }
@keyframes pulse { from { opacity: 1; } to { opacity: 0.4; } }
button.opening { color: #ffffff; animation: pulse 0.7s ease-in-out infinite alternate; }
label.status { color: #8e8e95; font-size: 16px; margin: 0 16px; }
"""
NARROW = b"button { min-width: 0; padding: 0 10px; margin: 12px 2px; } label.status { font-size: 14px; margin: 0 6px; }"


def xdo(*args):
    return subprocess.run(['xdotool'] + list(args), capture_output=True, text=True).stdout.split()


def fit(win):
    """Make an app window fill the screen above the dock (X11 apps ignore the dock's strut)."""
    try:
        sw, sh = map(int, xdo('getdisplaygeometry'))
        g = dict(l.split('=', 1) for l in subprocess.run(['xdotool', 'getwindowgeometry', '--shell', win],
                 capture_output=True, text=True).stdout.split())
        x, y, w, h = (int(g[k]) for k in ('X', 'Y', 'WIDTH', 'HEIGHT'))
    except (ValueError, KeyError):
        return
    hints = subprocess.run(['xprop', '-id', win, '_MOTIF_WM_HINTS'], capture_output=True, text=True).stdout
    if '0x2, 0x0, 0x0' not in hints:  # no title bar: no close or minimize buttons (apps can turn it back on)
        subprocess.run(['xprop', '-id', win, '-f', '_MOTIF_WM_HINTS', '32c', '-set', '_MOTIF_WM_HINTS', '2, 0, 0, 0, 0'])
        x = -1  # size it again: the frame changed
    if (x, y, w, h) != (0, 0, sw, sh - HEIGHT):
        xdo('windowstate', '--remove', 'FULLSCREEN', win)
        xdo('windowstate', '--remove', 'MAXIMIZED_VERT', win)
        xdo('windowstate', '--remove', 'MAXIMIZED_HORZ', win)
        xdo('windowmove', win, '0', '0')
        xdo('windowsize', win, str(sw), str(sh - HEIGHT))


def windows(wmclass):
    """The visible windows of the app, biggest first."""
    out = []
    # Only top-level windows that the window manager manages (Java apps also have big inner windows).
    managed = {str(int(l.split()[0], 16)) for l in subprocess.run(['wmctrl', '-l'], capture_output=True,
               text=True).stdout.splitlines() if l.strip()}
    for win in xdo('search', '--onlyvisible', '--class', wmclass):
        if win not in managed:
            continue
        try:
            g = dict(l.split('=', 1) for l in subprocess.run(['xdotool', 'getwindowgeometry', '--shell', win],
                     capture_output=True, text=True).stdout.split())
            a = int(g['WIDTH']) * int(g['HEIGHT'])
        except (ValueError, KeyError):
            continue
        out.append((a, win))
    return [w for a, w in sorted(out, reverse=True)]


def main_window(wmclass):
    """The biggest visible window of the app (not a dialog or a helper window)."""
    return (windows(wmclass) or [None])[0]


def raise_app(wmclass):
    win = main_window(wmclass)
    if win:
        fit(win)
        xdo('windowactivate', win)
    return win


def state(unit):
    return subprocess.run(['systemctl', '--user', 'is-active', unit], capture_output=True, text=True).stdout.strip()


def running(unit):
    """Also while it starts or quits: never two heavy apps at the same time."""
    return state(unit) not in ('inactive', 'failed', '')


def start(app):
    label, unit, wmclass, cmd = app
    if cmd:  # a transient unit, so 70-daily.sh can count the time
        subprocess.Popen(['systemd-run', '--user', '--quiet', '--collect', '--unit=' + unit] + cmd)
    else:
        subprocess.Popen(['systemctl', '--user', 'start', unit])
    # Raise it when its window shows: try every 0.5 s for 2 min. Then its button stops saying "Opening…".
    opening[0] = app
    last_start[0] = GLib.get_monotonic_time()
    deadline[0] = GLib.get_monotonic_time() + 120_000_000

    def wait():
        if raise_app(wmclass) or GLib.get_monotonic_time() > deadline[0]:
            opening[0] = None
            return False
        return True
    GLib.timeout_add(500, wait)


def close(app):
    """Ask the app to close, like the window's close button: it shows its own "Save changes?" dialog.
    All its main windows (Krita can have two), not dialogs: a dialog belongs to a window (WM_TRANSIENT_FOR)."""
    wins = [w for w in windows(app[2]) if 'window id' not in
            subprocess.run(['xprop', '-id', w, 'WM_TRANSIENT_FOR'], capture_output=True, text=True).stdout]
    for win in wins:
        subprocess.run(['wmctrl', '-ic', hex(int(win))])
    if not wins:
        subprocess.run(['systemctl', '--user', 'stop', app[1]])


def show(button, app):
    """One app at a time (less memory): close the open app, then start the one she tapped.
    The open app may ask "Save changes?". If she cancels, it stays open; a new tap asks again.
    The button says "Opening…" only when the app starts, so a cancel leaves no stale label."""
    if busy():
        return  # one start at a time: systemd may not know the new unit yet, so wait until its window shows
    if app is not APPS[0]:
        drop(KRITA_FILE)  # a picture for Krita: only for a switch to Krita
    if running(app[1]):
        switching[0] = None
        raise_app(app[2])
        return
    for a in APPS:
        if a is not app and running(a[1]):
            close(a)
    waiting = switching[0] is not None
    switching[0] = app
    give_up[0] = GLib.get_monotonic_time() + 300_000_000  # time to answer "Save changes?"
    if waiting:
        return  # the step below is already waiting; it now starts this app

    def step():
        target = switching[0]
        if target is None:
            return False
        if any(running(a[1]) for a in APPS if a is not target):  # wait until it quits (a big save can take long)
            if GLib.get_monotonic_time() < give_up[0]:
                return True
            switching[0] = opening[0] = None
            drop(KRITA_FILE)
            return False
        switching[0] = None
        start(target)
        return False
    GLib.timeout_add(500, step)


give_up = [0]
def busy():
    return opening[0] and (running(opening[0][1]) or GLib.get_monotonic_time() - last_start[0] < 10_000_000)


def drop(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def on_request(monitor, f, other, event):
    """The Library asks: open a file in Krita (one app at a time, so the dock does it)."""
    if event not in (Gio.FileMonitorEvent.CREATED, Gio.FileMonitorEvent.CHANGES_DONE_HINT,
                     Gio.FileMonitorEvent.MOVED_IN, Gio.FileMonitorEvent.RENAMED) or not os.path.exists(REQUEST):
        return
    try:
        os.replace(REQUEST, REQUEST + '.taken')  # take it first: a newer request then stays for the next event
        req = json.load(open(REQUEST + '.taken'))
    except (OSError, ValueError):
        return
    krita = APPS[0]
    if busy():  # an app starts now: the dock ignores this, she taps Open in Krita again
        return drop(REQUEST + '.taken')
    if state(krita[1]) == 'active' and not switching[0]:  # not while the dock closes it (a new Krita would start)
        subprocess.Popen(['krita', req['file']], env=dict(os.environ, QT_QPA_PLATFORM='xcb'))  # goes to the open Krita
        raise_app(krita[2])
    else:
        with open(KRITA_FILE, 'w') as fh:  # krita-open (the service) opens it
            fh.write(req['file'])
        show(None, krita)
    drop(REQUEST + '.taken')  # done: a .taken file at start means the dock stopped before this line


RUNDIR = os.path.join(GLib.get_user_runtime_dir(), 'art-kit')
REQUEST = os.path.join(RUNDIR, 'request.json')
KRITA_FILE = os.path.join(RUNDIR, 'krita-file')
switching = [None]  # the app the dock is switching to
opening = [None]  # the app that starts now: its button says "Opening…" until its window shows
last_start = [0]
deadline = [0]


def front_class():
    r = subprocess.run(['xdotool', 'getactivewindow', 'getwindowclassname'], capture_output=True, text=True)
    return r.stdout.strip().lower()


def mark(buttons):
    """Show which apps run and which one is in front."""
    import re
    if (not switching[0] and GLib.get_monotonic_time() - last_start[0] > 10_000_000
            and not any(running(a[1]) for a in APPS)):
        show(None, APPS[0])  # she quit the last app: open Krita again
    front = front_class()
    active = (xdo('getactivewindow') or [None])[0]
    for b, (label, unit, wmclass, cmd) in buttons:
        if active and re.search(wmclass, front) and main_window(wmclass) == active:
            fit(active)  # main windows that resize themselves go back above the dock; dialogs stay as they are
        on = subprocess.run(['systemctl', '--user', '-q', 'is-active', unit]).returncode == 0
        (b.add_css_class if on else b.remove_css_class)('running')
        (b.add_css_class if on and re.search(wmclass, front) else b.remove_css_class)('front')
        b.set_label('Opening…' if opening[0] and opening[0][0] == label else label)
        (b.add_css_class if opening[0] and opening[0][0] == label else b.remove_css_class)('opening')
    return True


def ago(t):
    m = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() // 60)
    return 'just now' if m < 1 else '%d min ago' % m if m < 60 else '%d h ago' % (m // 60) if m < 2880 else '%d days ago' % (m // 1440)


def backup_text():
    try:
        word, when = open(STATE).read().split()[:2]
        if word == 'ok':
            return '✓ Backed up ' + ago(datetime.datetime.fromisoformat(when))
        if word == 'sync':
            return '↻ Syncing'  # files still go up
    except (OSError, ValueError):
        pass
    return '✗ Not backed up'


def battery_text(upower):
    if upower is None:
        return ''
    pct = upower.get_cached_property('Percentage')
    present = upower.get_cached_property('IsPresent')
    if pct is None or present is None or not present.unpack():
        return ''
    return 'Battery %d%%' % pct.unpack()


def on_activate(app):
    if app.get_active_window():
        return
    provider = Gtk.CssProvider()
    mon = Gdk.Display.get_default().get_monitors().get_item(0)
    provider.load_from_data(CSS + (NARROW if mon and mon.get_geometry().width < 1200 else b''))  # portrait: all fits
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    box = Gtk.Box(spacing=0)
    box.add_css_class('dock')
    buttons = []
    for a in APPS:
        b = Gtk.Button(label=a[0])
        b.connect('clicked', show, a)
        b.connect('clicked', lambda *x: GLib.timeout_add(800, lambda: mark(buttons) and False))
        box.append(b)
        buttons.append((b, a))
    box.append(Gtk.Box(hexpand=True))
    battery = Gtk.Label(css_classes=['status'])
    backup = Gtk.Label(css_classes=['status'])
    box.append(battery)
    box.append(backup)
    try:
        upower = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SYSTEM, Gio.DBusProxyFlags.NONE, None, 'org.freedesktop.UPower',
            '/org/freedesktop/UPower/devices/DisplayDevice', 'org.freedesktop.UPower.Device', None)
        upower.connect('g-properties-changed', lambda *a: battery.set_text(battery_text(upower)))
    except GLib.Error:
        upower = None

    def update():
        battery.set_text(battery_text(upower))
        backup.set_text(backup_text())
        return True
    update()
    GLib.timeout_add_seconds(60, update)
    GLib.timeout_add_seconds(2, mark, buttons)  # apps can also close or come to front on their own

    os.makedirs(RUNDIR, exist_ok=True)
    monitor = Gio.File.new_for_path(RUNDIR).monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, None)
    monitor.connect('changed', on_request)
    app.monitor = monitor  # keep it alive

    win = Gtk.ApplicationWindow(application=app, title='Dock', decorated=False, resizable=False)
    win.set_default_size(mon.get_geometry().width if mon else 1280, HEIGHT)
    win.set_child(box)
    win.present()
    show(None, APPS[0])  # start with Krita in front
    # A request from before this start (the dock restarted): do it now.
    if not os.path.exists(REQUEST) and os.path.exists(REQUEST + '.taken'):
        os.replace(REQUEST + '.taken', REQUEST)
    on_request(None, None, None, Gio.FileMonitorEvent.CREATED)


app = Gtk.Application(application_id='org.artkit.Dock')
app.connect('activate', on_activate)
app.run([])
