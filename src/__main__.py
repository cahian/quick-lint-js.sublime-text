from .underlines import add_underlines
from .popup import add_popup


# TODO: Before send buffer, update diagnostics or not.
def on_load(buffer):
    views = buffer.views()
    diagnostics = buffer.diagnostics()
    add_underlines(views, diagnostics)


def on_unload(buffer):
    buffer.close()


def on_modify(buffer):
    on_load(buffer)
#     views = buffer.views()
#     diagnostics = buffer.diagnostics()
#     add_underlines(views, diagnostics)


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
