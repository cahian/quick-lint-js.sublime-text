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
    flags = DRAW_SQUIGGLY_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE
    regions = get_regions_by_severity(diagnostics)
    for view in views:
        # If warning regions and error regions overlap, error regions must have
        # priority over warning regions. For this to happen, we add the error
        # regions after the warning regions.
        view.add_regions("2", regions["warnings"], "region.orangish", "", flags)
        view.add_regions("1", regions["errors"], "region.redish", "", flags)
