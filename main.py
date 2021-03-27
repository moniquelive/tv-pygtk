import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk


@Gtk.Template.from_file("main.glade")
class AppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "main_app_window"

    btnSingle: Gtk.Button = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def btnSingle_clicked_cb(self, widget, **kwargs):
        assert self.btnSingle == widget
        print(widget.get_label(), kwargs)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="dev.monique.Gtk1",
                         flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        self.window = None

    def do_activate(self):
        self.window = self.window or AppWindow(application=self, title="Main Window")
        self.window.present()


if __name__ == '__main__':
    Application().run(sys.argv)
