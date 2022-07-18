"""This modules calls QuickLintJsListener methods pipipi popopo"""

from sublime_plugin import EventListener, ViewEventListener, TextChangeListener

from . import main
from .utils import is_javascript, remove_duplicates


class EngineEventListener(EventListener):
    # We need to manually filter the views with is_applicable.
    @classmethod
    def is_applicable(cls, view):
        return is_javascript(view.settings())

    def on_init(self, views):
        views = [view for view in views if self.is_applicable(view)]
        buffers = remove_duplicates([view.buffer() for view in views])
        main.on_init(buffers)


class EngineViewEventListener(ViewEventListener):
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

    def on_post_save(self):
        main.on_post_save(self.view)

    def on_hover(self):
        main.on_hover(self.view)


class EngineTextChangeListener(TextChangeListener):
    # The Sublime Text will automatically filter the buffers with is_applicable.
    @classmethod
    def is_applicable(cls, buffer):
        settings = buffer.primary_view().settings()
        return is_javascript(settings)

    def on_text_changed_async(changes):
        pass
