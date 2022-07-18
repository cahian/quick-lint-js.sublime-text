# Copyright (C) 2020  Matthew "strager" Glazar
# See end of file for extended copyright information.

class Buffer:
    """The represetation of a text buffer. Multiple view may share the same buffer.

    Just for the sake of clarity, you can think of a buffer as a block of memory
    that contains the file's text and a view as a tab in the Sublime Text.
    """
    def __init__(self, primary_view):
        self.views = [primary_view]  # TODO: {view} or [view]?
        self.parser = Parser(primary_view)

    def add_view(self, view):
        self.views.append(view)

    def remove_view(self, view):
        self.views.remove(view)


class BuffersManager:
    """PiPiPi PoPoPo!

    The internal strategy used is to share information between all views that
    belong to the same buffer. Because that way, if there are multiple views/tabs
    of the same buffer/file, they will all apply the same changes (have squiggly
    underlines and pop-ups available).
    """

    def __init__(self):
        self._buffers = {}

    def add_view(self, view):
        try:
            bid = view.buffer_id()
        except AttributeError:
            return
        if bid in self._buffers:
            self._buffers[bid].add_view(view)
        else:
            self._buffers[bid] = Buffer(view)
        return self._buffers[bid]

    def remove_view(self, view):
        try:
            bid = view.buffer_id()
        except AttributeError:
            return
        if bid in self._buffers:
            self._buffers[bid].remove_view(view)
        else:
            del self._buffers[bid]


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
