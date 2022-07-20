from sublime_plugin import EventListener, ViewEventListener, TextChangeListener

from .listeners import BufferEventListener


class BufferEventEmitter:
    listeners = {}

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


class EventEmitter(EventListener):
    # We need to manually filter the views with is_applicable.
    @classmethod
    def is_applicable(cls, view):
        return is_javascript(view.settings())

    def on_init(self, views):
        views = [view for view in views if self.is_applicable(view)]
        buffers = remove_duplicates([view.buffer() for view in views])
        bele.emit("on_init", buffers)


class ViewEventEmitter(ViewEventListener):
    # The Sublime Text will automatically filter the views with is_applicable.
    @classmethod
    def is_applicable(cls, settings):
        return is_javascript(settings)

    def on_close(self):
        main.on_close(self.view.buffer())

    def on_load_async(self):
        main.on_load_async(self.view.buffer())

    def on_reload_async(self):
        main.on_reload_async(self.view.buffer())

    def on_revert_async(self):
        main.on_revert_async(self.view.buffer())

    def on_clone_async(self):
        main.on_clone_async(self.view)

    def on_post_save_async(self):
        main.on_post_save_async(self.view)

    def on_hover(self, point, hover_zone):
        main.on_hover(self.view, point, hover_zone)


class TextChangeEmitter(TextChangeListener):
    # The Sublime Text will automatically filter the buffers with is_applicable.
    @classmethod
    def is_applicable(cls, buffer):
        settings = buffer.primary_view().settings()
        return is_javascript(settings)

    def on_text_changed_async(changes):
        main.on_text_changed_async(this.buffer, changes)


# """
# An Emitter can both listen to events and emit events.
# A Listener can only listen to events.
# """
