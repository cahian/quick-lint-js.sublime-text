"""The ideia of this modules is to allow the user have a similar experience with the listeners that sublime_plugin provides by
default."""


class BufferEventListener:
    pass


def get_listeners(cls):
    return cls.__subclasses__()


# """
# An Emitter can both listen to events and emit events.
# A Listener can only listen to events.
# """


# def _emit():
#     pass
#     # for listener in LISTENERS:
#     #     listener.i


# Here we will listen the Sublime Text events and emits them again. # to BufferEventListeners.


# """This modules calls QuickLintJsListener methods pipipi popopo"""
#
#
# from os.path import basename, dirname, realpath, splitext, join, isfile
# from glob import glob
# from importlib import import_module
# from inspect import getmembers, isclass
#
# from .list import remove_duplicates
# from .module import get_modules_from_directory
# from . import aa
