from sublime import DRAW_SQUIGGLY_UNDERLINE, DRAW_NO_FILL, DRAW_NO_OUTLINE


def get_regions_by_severity(diagnostics):
    regions = {"errors": [], "warnings": []}
    for diagnostic in diagnostics:
        if diagnostic.severity == Severity.error:
            regions["errors"].append(diagnostic.region)
        elif diagnostic.severity == Severity.warning:
            regions["warnings"].append(diagnostic.region)
    return regions


def add_squiggly_underlines(views, diagnostics):
    FLAGS = DRAW_SQUIGGLY_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE
    regions = get_regions_by_severity(diagnostics)
    for view in views:
        view.add_regions("2", regions["warnings"], "region.orangish", "", FLAGS)
        # TODO: Error regions can overlay warning regions.
        view.add_regions("1", regions["errors"], "region.redish", "", FLAGS)


def on_load(buffer):
    views = buffer.views()
    parser = buffer.parser()
    diagnostics = parser.diagnostics()
    add_squiggly_underlines(views, diagnostics)


def on_unload():
    pass


def on_clone(view):
    pass


def on_modified(buffer, change):  # NOTE: change can be None
    pass


def on_hover_text(view, point):
    pass
