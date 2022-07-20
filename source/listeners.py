"""This modules calls QuickLintJsListener methods pipipi popopo"""


from os.path import basename, dirname, realpath, splitext, join, isfile
from glob import glob
from importlib import import_module
from inspect import getmembers, isclass

from sublime_plugin import EventListener, ViewEventListener, TextChangeListener

from .list import remove_duplicates


__dirname__ = dirname(__file__)


def getmodname(path):
    return basename(path)[:-3]


def ismodname(path):
    return entry[-3:] == ".py"


def listmod(path):
    for entry in listdir(path):
        if isfile(entry) and ismodname(entry):
            yield modname(entry)


def import_modules_from_directory(directory):
    for modname in listmod(directory):
        yield import_module(modname)


def import_modules_from_directory(dir):
    modules = []
    for filename in glob(join(directory, "*.py")):
        modulename = splitext(basename(filename))[0]
        if isfile(filename) and modulename != __name__:
            modules.append(import_module(modulename))

    for entry in listdir(dir):
        if entry
    return modules


def get_listeners(modules):
    listeners = []
    for module in modules:
        for name, object in getmembers(module):
            if isclass(object) and issubclass(object, BufferEventListener) and BufferEventListener != object:
                listeners.append(object)
    return listeners


LISTENERS = []


class BufferEventListener:
    pass


# Here we will listen the Sublime Text events and emits them again. # to BufferEventListeners.


class EventEmitter(EventListener):
    # We need to manually filter the views with is_applicable.
    @classmethod
    def is_applicable(cls, view):
        return is_javascript(view.settings())

    def on_init(self, views):
        views = [view for view in views if self.is_applicable(view)]
        buffers = remove_duplicates([view.buffer() for view in views])
        main.on_init(buffers)


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
