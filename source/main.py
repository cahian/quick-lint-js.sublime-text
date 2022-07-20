from sublime import HOVER_TEXT

from .listeners import BufferEventListener
from .interface import Document
from .underlines import add_underlines, remove_underlines
from .popup import add_popup
from .syntax import is_javascript


# TODO: Reduce code repetition.
class QuickLintJsBufferEventListener(BufferEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return is_javascript(settings)

    def on_init(self):
        self.document = Document()

    def on_exit(self):
        self.document.close()

    def on_load_async(self):
        try:
            views = self.buffer.views()
            diagnostics = self.document.lint_from_buffer(self.buffer)
            add_underlines(views, diagnostics)
        except DocumentError as docerror:
            try:
                docerror.display_message()
            except:
                pass
        finally:
            remove_underlines()

    def on_clone_async(self, view):
        try:
            diagnostics = self.document.lint_from_view(view)
            add_underlines([view], diagnostics)
        except DocumentError as docerror:
            try:
                docerror.display_message()
            except:
                pass
        finally:
            remove_underlines()

    def on_text_changed_async(self, change):
        try:
            views = self.buffer.views()
            diagnostics = self.document.lint_from_changes(changes)
            add_underlines(views, diagnostics)
        except DocumentError as docerror:
            try:
                docerror.display_message()
            except:
                pass
        finally:
            remove_underlines()

    def on_hover(self, point, hover_zone):
        if hover_zone == HOVER_TEXT:
            diagnostics = self.document.diagnostics()
            for diagnostic in diagnostics:
                # If the user hovers over the diagnostic region
                # (region with underlines).
                if diagnostic.region.contains(point):
                    add_popup(view, diagnostic)


# def on_init(buffers):
#     pass
#
#
# def on_close(buffer):
#     buffer.close()
#
#
# # TODO: Before send buffer, update diagnostics or not.
# def on_load(buffer):
#     views = buffer.views()
#     diagnostics = buffer.diagnostics()
#     add_underlines(views, diagnostics)
#
#
# def on_modify(buffer, change):
#     on_load(buffer)
#     views = buffer.views()
#     diagnostics = buffer.diagnostics_from_change(change)
#     add_underlines(views, diagnostics)
#
#
# def on_clone(buffer, view):
#     diagnostics = buffer.diagnostics()
#     add_underlines([view], diagnostics)
#
#
# def on_hover_text(buffer, view, point):
#     diagnostics = buffer.diagnostics()
#     for diagnostic in diagnostics:
#         # If the user hovers over the diagnostic region (region
#         # with underlines).
#         if diagnostic.region.contains(point):
#             add_popup(view, diagnostic)
#
#
    # def on_close(self):
    #     views = self.buffer.views()
    #     if views:
    #         self.on_exit()

    # def on_post_save_async(self):
    #     self.on_init()


    # def on_reload_async(self):
    #     self.on_init()

    # def on_revert_async(self):
    #     self.on_init()
