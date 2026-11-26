#!/usr/bin/env python3
"""Art Kit dock: one bar at the bottom of the screen (GNOME Kiosk places it: window-config.ini).
Buttons: Krita, Sweet Home 3D, Blender, Library. Right side: battery and backup state.
A tap starts the app if it does not run (as a systemd user unit: 70-daily.sh counts unit time), then raises it.
"""
import datetime, subprocess
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
CSS = b"""
window, .dock { background: linear-gradient(#6b4423, #4a2c14); }
button { min-height: 52px; min-width: 150px; margin: 6px; padding: 0 12px; font-size: 20px; font-weight: bold;
         color: #f3d27a; background: #3a2210; border: 2px solid #b8860b; border-radius: 10px; }
button:active { background: #b8860b; color: #3a2210; }
label.status { color: #f3d27a; font-size: 18px; margin: 0 14px; }
"""


def show(button, app):
    label, unit, wmclass, cmd = app
    if subprocess.run(['systemctl', '--user', '-q', 'is-active', unit]).returncode != 0:
        if cmd:  # a transient unit, so 70-daily.sh can count the time
            subprocess.Popen(['systemd-run', '--user', '--quiet', '--collect', '--unit=' + unit] + cmd)
        else:
            subprocess.Popen(['systemctl', '--user', 'start', unit])
    # Raise the window. --sync waits until a new window shows (2 min at most).
    subprocess.Popen(['timeout', '120', 'xdotool', 'search', '--sync', '--onlyvisible', '--class', wmclass,
                      'windowactivate'], stderr=subprocess.DEVNULL)


def ago(t):
    m = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() // 60)
    return 'just now' if m < 1 else '%d min ago' % m if m < 60 else '%d h ago' % (m // 60) if m < 2880 else '%d days ago' % (m // 1440)


def backup_text():
    try:
        word, when = open(STATE).read().split()[:2]
        if word == 'ok':
            return '✓ Backed up ' + ago(datetime.datetime.fromisoformat(when))
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
    provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    box = Gtk.Box(spacing=0)
    box.add_css_class('dock')
    for a in APPS:
        b = Gtk.Button(label=a[0])
        b.connect('clicked', show, a)
        box.append(b)
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

    win = Gtk.ApplicationWindow(application=app, title='Dock', decorated=False, resizable=False)
    mon = win.get_display().get_monitors().get_item(0)
    win.set_default_size(mon.get_geometry().width if mon else 1280, HEIGHT)
    win.set_child(box)
    win.present()
    show(None, APPS[0])  # start with Krita in front


app = Gtk.Application(application_id='org.artkit.Dock')
app.connect('activate', on_activate)
app.run([])
