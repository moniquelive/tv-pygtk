import sys
import threading

import gi
import redis

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import GLib, Gdk, Gio, Gtk

redisSetKey = "moniquelive_bot:roster"
redisChannel = 'moniquelive_bot:notifications'

red = redis.Redis(host='127.0.0.1')
pubsub = redis.Redis(host='127.0.0.1').pubsub()
pubsub.subscribe([redisChannel])


@Gtk.Template.from_file("main.glade")
class AppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "main_app_window"

    lblCount: Gtk.Label = Gtk.Template.Child()
    lblResult: Gtk.Label = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def main_app_window_window_state_event_cb(self, _widget, state: Gdk.EventWindowState):
        s: Gdk.WindowState = state.new_window_state
        created = len(s.value_names) == 1 and s.value_names[0] == 'GDK_WINDOW_STATE_FOCUSED'
        if created:
            thread = threading.Thread(target=self.do_refresh)
            thread.daemon = True
            thread.start()

    def do_refresh(self):
        for _ in pubsub.listen():
            GLib.idle_add(self.lblResult.set_text, '...')
            GLib.idle_add(self.lblCount.set_text, '0 doidos')
            roster = red.smembers(redisSetKey)
            roster = sorted([x.decode('utf-8') for x in roster])
            GLib.idle_add(self.lblResult.set_text, '\n'.join(roster))
            GLib.idle_add(self.lblCount.set_text, f"{len(roster)} doidos")


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="dev.monique.bot.Roster",
                         flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        self.window = None

    def do_activate(self):
        self.window = self.window or AppWindow(application=self)
        self.window.present()


if __name__ == '__main__':
    Application().run(sys.argv)
