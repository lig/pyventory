class PyventoryError(Exception):
    pass


class PropertyIsNotImplementedError(PyventoryError):
    pass


class ValueSubstitutionError(PyventoryError):
    pass


class ValueSubstitutionInfiniteLoopError(PyventoryError):
    pass
