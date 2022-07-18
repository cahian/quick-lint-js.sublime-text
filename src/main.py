from .underlines import add_underlines
from .popup import add_popup


class QuickLintJsListener:
    pass


def on_init(buffers):
    pass


def on_close(buffer):
    buffer.close()


# TODO: Before send buffer, update diagnostics or not.
def on_load(buffer):
    views = buffer.views()
    diagnostics = buffer.diagnostics()
    add_underlines(views, diagnostics)


def on_modify(buffer, change):
    on_load(buffer)
    views = buffer.views()
    diagnostics = buffer.diagnostics_from_change(change)
    add_underlines(views, diagnostics)


def on_clone(buffer, view):
    diagnostics = buffer.diagnostics()
    add_underlines([view], diagnostics)


def on_hover_text(buffer, view, point):
    diagnostics = buffer.diagnostics()
    for diagnostic in diagnostics:
        # If the user hovers over the diagnostic region (region
        # with underlines).
        if diagnostic.region.contains(point):
            add_popup(view, diagnostic)
