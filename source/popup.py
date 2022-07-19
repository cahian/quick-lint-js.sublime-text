from html import escape

from sublime import HIDE_ON_MOUSE_MOVE_AWAY


def add_popup(view, diagnostic):

    message = diagnostic.message
    code = diagnostic.code
    color = view.style_for_scope("comment.line")["foreground"]

    minihtml = """
    <body style="margin: 0.8rem;">
        <div>%s</div>
        <div style="color: %s;">quick-lint-js(%s)</div>
    </body>
    """
    content = minihtml % (escape(message), escape(color), escape(code))

    flags = HIDE_ON_MOUSE_MOVE_AWAY
    location = diagnostic.region.begin()
    max_width, max_height = (1280, 720)  # 1280x720 Screen Resolution
    self.view.show_popup(content, flags, location, max_width, max_height)
