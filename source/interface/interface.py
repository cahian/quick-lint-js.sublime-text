"""Middleware between the quick-lint-js and the plugin"""

# NOTE: There is some way to avoid plugin crashes and raise exceptions?
# NOTE: This class is needed?
class DocumentError(Exception):
    pass


class Document:
    def full_update(buffer):
        pass

    def incremental_update(changes):
        pass

    def lint():
        pass

    def diagnostics():
        pass
