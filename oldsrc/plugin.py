# Copyright (C) 2020  Matthew "strager" Glazar
# See end of file for extended copyright information.

import html

import sublime

from .buffer import BuffersManager
from .interface import Parser
from .utils import is_js


bmanager = BuffersManager()


class QljsViewEventListener(ViewEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return Parser.is_working() and is_js(settings)

    @classmethod
    def applies_to_primary_view_only(cls):
        return False

    def


class QljsBaseListener:
    def __init__(self, view):
        # TODO: if view: ???
        self.view = view
        self.buffer = bmanager.add_view(self.view)

    def __del__(self):
        # TODO: if hasattr(self, "view"): ???
        bmanager.remove_view(self.view)

    def add_squiggly_underlines(self):
        error_regions, warning_regions = self.get_regions_by_severity()
        flags = (
            sublime.DRAW_SQUIGGLY_UNDERLINE
            | sublime.DRAW_NO_FILL
            | sublime.DRAW_NO_OUTLINE
        )
        for view in self.buffer.views:
            view.add_regions("2", warning_regions, "region.orangish", "", flags)
            # TODO: Error regions can overlay warning regions.
            view.add_regions("1", error_regions, "region.redish", "", flags)

    def remove_squiggly_underlines(self):
        for view in self.buffer.views:
            view.erase_regions("2")
            view.erase_regions("1")

    def get_regions_by_severity(self):
        error_regions = []
        warning_regions = []
        for diagnostic in self.buffer.parser.diagnostics:
            if diagnostic.severity == Severity.error:
                error_regions.append(diagnostic.region)
            elif diagnostic.severity == Severity.warning:
                warning_regions.append(diagnostic.region)
        return error_regions, warning_regions


class QljsBaseViewEventListener(QljsBaseListener):
    @classmethod
    def is_applicable(cls, settings):
        return QljsBaseListener.is_applicable(cls, settings)

    @classmethod
    def applies_to_primary_view_only(cls):
        return QljsBaseListener.applies_to_primary_view_only(cls)

    def __init__(self, view):
        QljsBaseListener.__init__(self, view)
        self.on_load()

    def on_load(self):
        try:
            self.buffer.parser.set_text()
            self.buffer.parser.lint()
            self.add_squiggly_underlines(self.buffer.parser.diagnostics)
        except ParserError as error:
            self.remove_squiggly_underlines()
            try:
                error.display_message()
            except ParserMessageError as error:
                pass

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


if interface.has_incremental_changes():

    from sublime_plugin import ViewEventListener, TextChangeListener

    class QljsViewEventListener(QljsBaseListener, ViewEventListener):
        pass


    class QljsTextChangeListener(QljsBaseListener, TextChangeListener):
        @classmethod
        def is_applicable(cls, buffer):
            settings = buffer.primary_view().settings()
            return QljsBaseListener.is_applicable(cls, settings)

        def __init__(self):
            QljsBaseListener.__init__(self, None)
            TextChangeListener.__init__(self)

        def on_text_changed(self, changes):
            self.buffer = bmanager.get_buffer(self.buffer.id())
            try:
                for change in changes:
                    self.buffer.parser.replace_text(change)
                self.buffer.parser.lint()
                self.add_squiggly_underlines()
            except ParserError as error:
                self.remove_squiggly_underlines()
                if error.has_message():
                    error.display_message()

else:

    from sublime_plugin import ViewEventListener

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
