from html import escape

from sublime import HIDE_ON_MOUSE_MOVE_AWAY


def add_popup(view, diagnostic):
    content = """
    <body style="margin: 0.8rem;">
        <div>{message}</div>
        <div style="color: {color};">quick-lint-js({code})</div>
    </body>
    """.format(
        message=diagnostic.message,
        code=diagnostic.code,
        color=view.style_for_scope("comment.line")["foreground"],
    )
    flags = HIDE_ON_MOUSE_MOVE_AWAY
    location = diagnostic.region.begin()
    max_width, max_height = (1280, 720)  # These numbers are arbitrary.
    view.show_popup(content, flags, location, max_width, max_height)
