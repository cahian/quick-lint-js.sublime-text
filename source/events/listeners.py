"""This modules calls QuickLintJsListener methods pipipi popopo"""


from os.path import basename, dirname, realpath, splitext, join, isfile
from glob import glob
from importlib import import_module
from inspect import getmembers, isclass

from .list import remove_duplicates
from .module import get_modules_from_directory
from . import aa


class Config:
    listeners_directory = dirname(__file__)

    def set_listeners_directory(listeners_directory):
        self.listeners_directory = listeners_directory


def is_module_name(path):
    return entry[-3:] == ".py"


def get_module_name(path):
    return basename(path)[:-3]


def list_modules(path):
    for entry in listdir(path):
        if isfile(entry) and is_module_name(entry):
            yield get_module_name(entry)


def import_modules_from_directory(directory):
    for module_name in list_modules(directory):
        yield import_module(module_name)


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
    current_module_directory = dirname(__file__)
    modules = import_modules_from_directory(current_module_directory)
    classes = get_classes_from_modules(modules)

    listeners = []
    for module in modules:
        for name, object in getmembers(module):
            if isclass(object) and issubclass(object, BufferEventListener) and BufferEventListener != object:
                listeners.append(object)

    return listeners


CLASSES = get_classes_from_modules(MODULES)
LISTENERS = get_listeners_from_classes(CLASSES)


class BufferEventListener:
    pass


class BufferEventListenerManager:
    pass
# Here we will listen the Sublime Text events and emits them again. # to BufferEventListeners.


def _emit():
    pass
    # for listener in LISTENERS:
    #     listener.i
