# Copyright (C) 2020  Matthew "strager" Glazar
# See end of file for extended copyright information.

# TODO: Very importart that you test if has async method and if not use normal method
# TODO: Replace all top-level functions by classes
# TODO: Create 3 files: utils, cinterface, plugin
# TODO: self.diags or return?
# TODO: views = set or list?

import html

import sublime
from sublime_plugin import ViewEventListener, TextChangeListener

from .interface import aa


def is_js(settings):
    return "JavaScript" in settings.get("syntax", "")


class Buffer:
    """
# Just for the sake of clarity, you can think of a buffer as a block of memory
# that contains the file's text and a view as a tab in the sublime text.
    """
    def __init__(self, view):
        self.views = [view]  # TODO: {view} or [view]?
        self.parser = Parser(view)


class BuffersManager:
    """
# The internal strategy used is to share information between all views that
# belong to the same buffer. Because that way, if there are multiple views/tabs
# of the same buffer/file, they will all apply the same changes (have squiggly
# underlines and pop-ups available).
    """

    def __init__(self):
        self.buffers = {}

    def add_view(self, view):
        bid = view.buffer_id()
        if bid not in self.buffers:
            self.buffers[bid] = Buffer(view)
        else:
            self.buffers[bid].views.append(view)
        return self.buffers[bid]

    def remove_view(self, view):
        bid = view.buffer_id()
        self.buffers[bid].views.remove(view)
        if not self.buffers[bid].views:
            del self.buffers[bid]


bmanager = BuffersManager()


class QljsBaseListener:
    @classmethod
    def is_applicable(cls, settings):
        return Parser.is_working() and is_js(settings)

    @classmethod
    def applies_to_primary_view_only(cls):
        return False

    def __init__(self, view):
        if view:
            self.view = view
            self.buffer = bmanager.add_view(self.view)

    def __del__(self):
        if hasattr(self, "view"):
            bmanager.remove_view(self.view)

    def add_squiggly_underlines(self):
        warning_regions, error_regions = self.get_regions_by_severity()
        flags = (
            sublime.DRAW_SQUIGGLY_UNDERLINE
            | sublime.DRAW_NO_FILL
            | sublime.DRAW_NO_OUTLINE
        )
        for view in self.buffer.views:
            view.add_regions("2", warning_regions, "region.orangish", "", flags)
            view.add_regions("1", error_regions, "region.redish", "", flags)

    def remove_squiggly_underlines(self):
        for view in self.buffer.views:
            view.erase_regions("2")
            view.erase_regions("1")

    def get_regions_by_severity(self):
        warning_regions = []
        error_regions = []
        for diagnostic in self.buffer.parser.diagnostics:
            if Severity.warning == diagnostic.severity:
                warning_regions.append(diagnostic.region)
            elif Severity.error == diagnostic.severity:
                error_regions.append(diagnostic.region)
        return warning_regions, error_regions


if interface.has_incremental_changes():

    class QljsViewEventListener(QljsBaseListener, ViewEventListener):
        @classmethod
        def is_applicable(cls, settings):
            return QljsBaseListener.is_applicable(cls, settings)

        @classmethod
        def applies_to_primary_view_only(cls):
            return QljsBaseListener.applies_to_primary_view_only(cls)

        def __init__(self, view):
            QljsBaseListener.__init__(self, view)
            ViewEventListener.__init__(self, view)
            self.on_load()

        def on_load(self):
            try:
                self.buffer.parser.set_text()
                self.buffer.parser.lint()
                self.add_squiggly_underlines()
            except Error as error:
                self.remove_squiggly_underlines()
                if error.has_message():
                    error.display_message()

        def on_reload(self):
            self.on_load()

        def on_revert(self):
            self.on_load()

        def on_hover(self, point, hover_zone):
            if hover_zone == sublime.HOVER_TEXT:
                for diagnostic in self.buffer.parser.diagnostics:
                    # If the user hovers over the diagnostic region
                    # (region with squiggly underlines).
                    if diagnostic.region.contains(point):
                        self.add_popup(diagnostic)

        def add_popup(self, diagnostic):
            minihtml = """
            <body style="margin: 0.8rem;">
                <div>%s</div>
                <div style="color: %s;">quick-lint-js(%s)</div>
            </body>
            """
            color = self.view.style_for_scope("comment.line")["foreground"]
            content = minihtml % (
                html.escape(diagnostic.message),
                html.escape(color),
                html.escape(diagnostic.code),
            )

            flags = sublime.HIDE_ON_MOUSE_MOVE_AWAY
            location = diagnostic.region.begin()
            max_width, max_height = (1280, 720)  # 1280x720 Screen Resolution
            self.view.show_popup(content, flags, location, max_width, max_height)

    class QljsTextChangeListener(TextChangeListener, QljsBaseListener):
        @classmethod
        def is_applicable(cls, buffer):
            if not Parser.is_working():
                return False
            settings = buffer.primary_view().settings()
            syntax = settings.get("syntax", "")
            return "JavaScript.sublime-syntax" in syntax

        def __init__(self):
            TextChangeListener.__init__(self)
            QljsBaseListener.__init__(self, None)

        def on_text_changed(self, changes):
            self.buffer = (
                bmanager.get_buffer(
                    self.buffer.id()
                )
            )
            try:
                for change in changes:
                    self.buffer.parser.replace_text(change)
                self.buffer.parser.lint()
                self.add_squiggly_underlines()
            except Error as error:
                self.remove_squiggly_underlines()
                if error.has_message():
                    error.display_message()

else:

    class QljsListener(ViewEventListener):
        @classmethod
        def is_applicable(cls, settings):
            return Parser.is_working() and is_js(settings)

        @classmethod
        def applies_to_primary_view_only(cls):
            return False

        def __init__(self, view):
            super().__init__(view)
            self.buffer = bmanager.add_view(self.view)
            self.on_modified()

        def __del__(self):
            bmanager.remove_view(self.view)

        def on_load(self):
            self.on_modified()

        def on_modified(self):
            try:
                self.buffer.parser.set_text()
                self.buffer.parser.lint()
                self.add_squiggly_underlines()
            except Error as error:
                self.remove_squiggly_underlines()
                if error.has_message():
                    error.display_message()

        def on_hover(self, point, hover_zone):
            if hover_zone == sublime.HOVER_TEXT:
                for diagnostic in self.buffer.parser.diagnostics:
                    # If the user hovers over the diagnostic region (region with
                    # squiggly underlines).
                    if diagnostic.region.contains(point):
                        self.add_popup(diagnostic)

        def add_squiggly_underlines(self):
            warning_regions, error_regions = self.get_regions_by_severity()
            flags = (
                sublime.DRAW_SQUIGGLY_UNDERLINE
                | sublime.DRAW_NO_FILL
                | sublime.DRAW_NO_OUTLINE
            )
            for view in self.buffer.views:
                view.add_regions("2", warning_regions, "region.orangish", "", flags)
                view.add_regions("1", error_regions, "region.redish", "", flags)

        def remove_squiggly_underlines(self):
            for view in self.buffer.views:
                view.erase_regions("2")
                view.erase_regions("1")

        def get_regions_by_severity(self):
            warning_regions = []
            error_regions = []
            for diagnostic in self.buffer.parser.diagnostics:
                if Severity.warning == diagnostic.severity:
                    warning_regions.append(diagnostic.region)
                elif Severity.error == diagnostic.severity:
                    error_regions.append(diagnostic.region)
            return warning_regions, error_regions

        def add_popup(self, diagnostic):
            minihtml = """
            <body style="margin: 0.8rem;">
                <div>%s</div>
                <div style="color: %s;">quick-lint-js(%s)</div>
            </body>
            """
            color = self.view.style_for_scope("comment.line")["foreground"]

            # Sublime Text 3 parser cannot interpret escaped quotes:
            # > Parse Error: quot; code: Unknown entity
            content = minihtml % (
                html.escape(diagnostic.message, quote=False),
                html.escape(color, quote=False),
                html.escape(diagnostic.code, quote=False),
            )

            flags = sublime.HIDE_ON_MOUSE_MOVE_AWAY
            location = diagnostic.region.begin()
            max_width, max_height = (1280, 720)  # 1280x720 Screen Resolution
            self.view.show_popup(content, flags, location, max_width, max_height)




# class Buffer:
#     def __init__(self, view):
#         self.views = {view}
#         self.parser = Parser(view)
#
#
# class BuffersManager:
#     def __init__(self):
#         self.buffers = {}
#
#     def add_view(self, view):
#         id_ = view.buffer_id()
#         if id_ not in self.buffers:
#             self.buffers[id_] = Buffer(view)
#         else:
#             self.buffers[id_].views.add(view)
#         return self.buffers[id_]
#
#     def remove_view(self, view):
#         id_ = view.buffer_id()
#         if id_ not in self.buffers:
#             return
#         self.buffers[id_].views.discard(view)
#         if not self.buffers[id_].views:
#             del self.buffers[id_]
#
#     def get_buffer(self, id_):
#         return self.buffers[id_]


# quick-lint-js finds bugs in JavaScript programs.
# Copyright (C) 2020  Matthew Glazar
#
# This file is part of quick-lint-js.
#
# quick-lint-js is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quick-lint-js is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with quick-lint-js.  If not, see <https://www.gnu.org/licenses/>.
