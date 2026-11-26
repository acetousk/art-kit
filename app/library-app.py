#!/usr/bin/env python3
"""Library app: one full-screen WebKit window, offline only.
All content comes from library:// (see library.py). No web server, no ports.
Usage: library-app.py [--root DIR]   (DIR holds Library/ and Art/; default: your home)
"""
import argparse, os, sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('WebKit', '6.0')
gi.require_version('Soup', '3.0')
from gi.repository import Gio, GLib, Gtk, Soup, WebKit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library import Library

# Only library: content. Blocks http, https, file, data scripts, and so on.
CSP = ("default-src library:; style-src library: 'unsafe-inline'; img-src library: data:; "
       "form-action 'none'; frame-src 'none'; object-src 'none'")


def launch(argv):  # non-blocking, the app does not wait for Krita
    Gio.Subprocess.new(argv, Gio.SubprocessFlags.NONE)


def on_request(req, lib):
    status, mime, body = lib.handle(req.get_uri())
    resp = WebKit.URISchemeResponse.new(Gio.MemoryInputStream.new_from_bytes(GLib.Bytes.new(body)), len(body))
    resp.set_content_type(mime)
    resp.set_status(status, None)
    h = Soup.MessageHeaders.new(Soup.MessageHeadersType.RESPONSE)
    h.append('Content-Security-Policy', CSP)
    h.append('Cache-Control', 'no-store')
    # The UI (library://ui) fetches data from library://api: WebKit needs this header for that.
    h.append('Access-Control-Allow-Origin', '*')
    resp.set_http_headers(h)
    req.finish_with_response(resp)


def on_policy(view, decision, kind):
    if kind == WebKit.PolicyDecisionType.RESPONSE:
        if not decision.is_mime_type_supported():  # would be a download
            decision.ignore()
            return True
        return False
    uri = decision.get_navigation_action().get_request().get_uri()
    if kind == WebKit.PolicyDecisionType.NEW_WINDOW_ACTION or not uri.startswith('library://'):
        decision.ignore()
        return True
    return False


def on_activate(app, lib):
    if app.get_active_window():  # dock tapped again: show the open window
        app.get_active_window().present()
        return
    session = WebKit.NetworkSession.new_ephemeral()
    session.connect('download-started', lambda s, d: d.cancel())
    # A dead proxy: if something slips past the checks, it still cannot reach a network.
    session.set_proxy_settings(WebKit.NetworkProxyMode.CUSTOM,
                               WebKit.NetworkProxySettings.new('http://127.0.0.1:9', None))
    ctx = WebKit.WebContext.new()
    ctx.register_uri_scheme('library', on_request, lib)
    sec = ctx.get_security_manager()
    sec.register_uri_scheme_as_secure('library')
    sec.register_uri_scheme_as_cors_enabled('library')

    settings = WebKit.Settings(enable_developer_extras=False, enable_javascript=True,
                               javascript_can_open_windows_automatically=False,
                               allow_file_access_from_file_urls=False,
                               allow_universal_access_from_file_urls=False,
                               enable_back_forward_navigation_gestures=False,
                               enable_webaudio=False, enable_webgl=False, enable_media=False)
    view = WebKit.WebView(web_context=ctx, network_session=session, settings=settings)
    view.connect('decide-policy', on_policy)
    view.connect('context-menu', lambda *a: True)        # no right-click menu
    view.connect('create', lambda *a: None)               # no new windows
    view.connect('web-process-terminated', lambda v, r: v.load_uri('library://ui/index.html'))
    view.load_uri('library://ui/index.html')

    win = Gtk.ApplicationWindow(application=app, title='Library')
    win.set_child(view)
    win.fullscreen()
    win.present()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.expanduser('~'), help='dir that holds Library/ and Art/')
    args = ap.parse_args()
    lib = Library(os.path.abspath(args.root), launch)
    app = Gtk.Application(application_id='org.artkit.Library')
    app.connect('activate', on_activate, lib)
    app.run([sys.argv[0]])


if __name__ == '__main__':
    main()
