"""Emitters are Listeners that emits again the events that they receives."""
"""Emitters are Listeners who re-emit the events they listen to."""
"""Emitters are Listeners who re-emit the events they listen to other listeners."""
# NOTE: """Emitters can only work in the root of the package"""

from sublime_plugin import EventListener, TextChangeListener

from .listeners import BufferEventListener, get_listeners
from .utilities import remove_duplicates


class BufferEventEmitter:
    listeners = get_listeners(BufferEventListener)
    instances = {}

    def on_init(self, buffers):
        for buffer in buffers:
            id = buffer.id()
            if not listeners[id]:
                listeners[id] = BufferEventListener(buffer)
                listeners[id].on_init()

    def on_exit(self, buffer):
        id = buffer.id()
        if listeners[id]:
            listeners[id].on_exit()
            del listeners[id]

    def on_load_async(self, buffer):
        id = buffer.id()
        if not listeners[id]:
            listeners[id] = BufferEventListener(buffer)
        listeners[id].on_load_async()

    def on_clone_async(self, buffer, view):
        id = buffer.id()
        if not listeners[id]:
            listeners[id] = BufferEventListener(buffer)
        listeners[id].on_clone_async(view)

    def on_text_changed_async(self, buffer, changes):
        id = buffer.id()
        if not listeners[id]:
            listeners[id] = BufferEventListener(buffer)
        listeners[id].on_text_changed_async(changes)

    def on_hover(self, buffer, point, hover_zone):
        id = buffer.id()
        if not listeners[id]:
            listeners[id] = BufferEventListener(buffer)
        listeners[id].on_hover(point, hover_zone)


bee = BufferEventEmitter()


class EventEmitter(EventListener):
    def on_init(self, views):
        buffers = [view.buffer() for view in views]
        buffers = remove_duplicates(buffers)
        bee.on_init(buffers)

    def on_exit(self):
        bee.on_exit()

    def on_close(self, view):
        buffer = view.buffer()
        if not buffer.views():
            bee.on_exit()

    def on_load_async(self, view):
        buffer = view.buffer()
        bee.on_load_async(buffer)

    def on_reload_async(self, view):
        buffer = view.buffer()
        bee.on_reload_async(buffer)

    def on_revert_async(self, view):
        buffer = view.buffer()
        bee.on_revert_async(buffer)

    def on_clone_async(self, view):
        buffer = view.buffer()
        bee.on_clone_async(buffer, view)

    def on_post_save_async(self):
        buffer = view.buffer()
        bee.on_post_save_async(self.view)

    def on_hover(self, view, point, hover_zone):
        buffer = view.buffer()
        bee.on_hover(buffer, view, point, hover_zone)


class ViewEventEmitter(ViewEventListener):
    # The Sublime Text will automatically filter the views with is_applicable.
    # @classmethod
    # def is_applicable(cls, settings):
    #     return is_javascript(settings)



class TextChangeEmitter(TextChangeListener):
    # The Sublime Text will automatically filter the buffers with is_applicable.
    @classmethod
    def is_applicable(cls, buffer):
        settings = buffer.primary_view().settings()
        return is_javascript(settings)

    def on_text_changed_async(changes):
        main.on_text_changed_async(this.buffer, changes)


    # We need to manually filter the views with is_applicable.
    # @classmethod
    # def is_applicable(cls, view):
    #     return is_javascript(view.settings())

        # views = [view for view in views if self.is_applicable(view)]
