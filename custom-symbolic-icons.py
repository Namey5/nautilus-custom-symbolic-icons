#!/usr/bin/env python3
#
# NAME: Custom Symbolic Icons — Nautilus Python Extension
# AUTHOR: Namey5
# VERSION: v1.1.0
# LICENSE: GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# NAME: Custom Symbolic Icons
# DESC: Customise symbolic icons for folders in Nautilus (i.e. bookmarks).
# INSTALL:
#   cp custom-symbolic-icons.py ~/.local/share/nautilus-python/extensions/
#   nautilus -q
# EXAMPLE:
#   gio set ~/Games metadata::custom-symbolic-icon applications-games-symbolic

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, GObject, Gtk, Nautilus  # pyright: ignore[reportAttributeAccessIssue]


class CustomSymbolicIcons(GObject.GObject, Nautilus.MenuProvider):
    __gtype_name__ = "CustomSymbolicIcons"

    CUSTOM_ICON_ATTRIBUTE = "metadata::custom-symbolic-icon"

    def __init__(self) -> None:
        super().__init__()

        self.application = Gio.Application.get_default()
        # Update whenever a new window is created.
        self.application.connect("window_added", self._process_tree)
        # First window has a delay before widgets are added, so need to wait a little.
        GLib.timeout_add(500, self._refresh_windows)

    def _refresh_windows(self) -> bool:
        for window in self.application.get_windows():
            self._process_tree(self.application, window)
        return False

    def _process_tree(self, application: Gio.Application, widget: Gtk.Widget) -> None:
        if type(widget).__name__ == "NautilusSidebarRow":
            self._update_icon(widget)
            return

        child = widget.get_first_child()
        while child is not None:
            self._process_tree(application, child)
            child = child.get_next_sibling()

    def _update_icon(self, widget: Gtk.Widget) -> None:
        try:
            icon = widget.get_property("start-icon")
            icon_names = icon.get_names()

            uri = widget.get_property("uri")
            file = Gio.File.new_for_uri(uri)
            file_info = file.query_info(self.CUSTOM_ICON_ATTRIBUTE, Gio.FileQueryInfoFlags.NONE)
            icon_name = file_info.get_attribute_as_string(self.CUSTOM_ICON_ATTRIBUTE)

            if icon_name is not None and (len(icon_names) == 0 or icon_name != icon_names[0]):
                print(f"[custom-symbolic-icons] adding icon '{icon_name}' to file '{uri}' (existing: {icon_names})", file=sys.stderr)
                # Limited manipulation of this list, so just always prepend if not the first icon.
                icon.prepend_name(icon_name)

                icon_widget = widget.get_template_child(
                    GObject.GType.from_name("NautilusSidebarRow"),
                    "start_icon_widget"
                )
                icon_widget.set_from_gicon(icon)
        except Exception as e:  # noqa: BLE001, F841, S110
            # print(f"[custom-symbolic-icons] error setting icon: '{e}'", file=sys.stderr)
            pass

    def get_file_items(self, files: list[Nautilus.FileInfo]) -> list[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]
        menuitem = Nautilus.MenuItem(
            name="CustomSymbolicIcons::icon-name",
            label="Set Symbolic Icon...",
        )
        menuitem.connect("activate", self._show_file_icon_setter, file)
        return [menuitem]

    def get_background_items(self, folder: Nautilus.FileInfo) -> list[Nautilus.MenuItem]:  # pyright: ignore[reportUnusedParameter]
        return []

    def _show_file_icon_setter(self, menuitem: Nautilus.MenuItem, file_info: Nautilus.FileInfo) -> None:  # pyright: ignore[reportUnusedParameter]
        file = Gio.File.new_for_uri(file_info.get_uri())
        file_query = file.query_info(self.CUSTOM_ICON_ATTRIBUTE, Gio.FileQueryInfoFlags.NONE)
        icon_name = file_query.get_attribute_as_string(self.CUSTOM_ICON_ATTRIBUTE)

        window = Gtk.Window.new()
        window.set_modal(True)
        window.set_transient_for(self.application.get_active_window())
        window.set_decorated(True)
        window.set_resizable(False)
        window.set_title("Symbolic Icon")

        box = Gtk.ListBox.new()
        window.set_child(box)

        entry = Adw.EntryRow.new()
        entry.set_title("Icon Name")
        entry.set_show_apply_button(True)
        if icon_name is not None:
            entry.set_text(icon_name)
        entry.connect("apply", self._set_file_icon, window, file)
        box.append(entry)

        window.present()

    def _set_file_icon(self, entry: Adw.EntryRow, window: Gtk.Window, file_info: Nautilus.FileInfo) -> None:
        file = Gio.File.new_for_uri(file_info.get_uri())
        if entry.get_text():
            print(f"[custom-symbolic-icons] setting icon '{entry.get_text()}' for file '{file.get_uri()}'", file=sys.stderr)
            file.set_attribute_string(self.CUSTOM_ICON_ATTRIBUTE, entry.get_text(), Gio.FileQueryInfoFlags.NONE)
        else:
            print(f"[custom-symbolic-icons] clearing icon for file '{file.get_uri()}'", file=sys.stderr)
            # Bug: No easy way to remove an icon name from the list, so this will take effect after restart.
            file.set_attribute(self.CUSTOM_ICON_ATTRIBUTE, Gio.FileAttributeType.INVALID, None, Gio.FileQueryInfoFlags.NONE)

        window.close()

        # This doesn't seem to always hit all windows... (maybe different applications?)
        self._refresh_windows()
