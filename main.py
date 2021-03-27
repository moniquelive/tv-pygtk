import sys
import threading

import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk


@Gtk.Template.from_file("main.glade")
class AppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "main_app_window"

    txtName: Gtk.Entry = Gtk.Template.Child()
    btnSearch: Gtk.Button = Gtk.Template.Child()
    lblResult: Gtk.Label = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def btnSearch_clicked_cb(self, widget, **_kwargs):
        assert self.btnSearch == widget
        self.txtName.set_sensitive(False)
        self.btnSearch.set_sensitive(False)

        name = self.txtName.get_text()
        thread = threading.Thread(target=self.do_request, args=(name,))
        thread.daemon = True
        thread.start()

    def do_request(self, name):
        url = 'https://api.genderize.io/?name=' + name

        print(f"Buscando pelo nome {name}...")
        response = requests.get(url).json()
        GLib.idle_add(self.txtName.set_sensitive, True)
        GLib.idle_add(self.btnSearch.set_sensitive, True)
        if 'error' in response:
            print("*** Error:", response['error'])
            return
        print(response)

        gender = response['gender']
        prob = response['probability']
        GLib.idle_add(self.lblResult.set_text, f"{name} is {gender} ({int(100 * prob)}% sure)")
        GLib.idle_add(self.txtName.set_text, "")
        GLib.idle_add(self.txtName.grab_focus)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="dev.monique.Gtk1",
                         flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        self.window = None

    def do_activate(self):
        self.window = self.window or AppWindow(application=self)
        self.window.present()


if __name__ == '__main__':
    Application().run(sys.argv)
