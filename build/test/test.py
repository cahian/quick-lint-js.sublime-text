import sublime
from sublime_plugin import TextChangeListener


class QljsListener(TextChangeListener):
    def on_text_changed_async(changes):
        for change in chages:
            print(change)
