def is_javascript(settings):
    return "JavaScript" in settings.get("syntax", "")


def remove_duplicates(list_):
    return list(set(list_))
