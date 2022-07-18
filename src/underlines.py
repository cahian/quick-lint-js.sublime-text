from sublime import DRAW_SQUIGGLY_UNDERLINE, DRAW_NO_FILL, DRAW_NO_OUTLINE


def get_regions_by_severity(diagnostics):
    regions = {"errors": [], "warnings": []}
    for diagnostic in diagnostics:
        if diagnostic.severity == Severity.error:
            regions["errors"].append(diagnostic.region)
        elif diagnostic.severity == Severity.warning:
            regions["warnings"].append(diagnostic.region)
    return regions


def add_underlines(views, diagnostics):
    FLAGS = DRAW_SQUIGGLY_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE
    regions = get_regions_by_severity(diagnostics)
    for view in views:
        view.add_regions("2", regions["warnings"], "region.orangish", "", FLAGS)
        # If the warning regions and error regions overlap, the error regions
        # will overwrite the warning ones.
        view.add_regions("1", regions["errors"], "region.redish", "", FLAGS)
