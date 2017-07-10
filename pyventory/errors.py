import six


class PyventoryError(Exception):

    def __str__(self):
        if not self.args or not isinstance(self.args[0], six.string_types):
            return super(PyventoryError, self).__str__()

        return self.args[0].format(*self.args[1:])


class ValueSubstitutionError(PyventoryError):
    pass


class PropertyIsNotImplementedError(PyventoryError):
    pass
