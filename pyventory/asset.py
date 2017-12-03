import re
from collections import Mapping, OrderedDict, Sequence

import six
from pyventory import errors

__all__ = ['Asset']


class Asset(object):
    _string_format_regex = re.compile(r'{([\w_]+)}')

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def _vars(self):
        return self.__build_vars(self, strict_format=True)

    @classmethod
    def _cls_vars(cls):
        return cls.__build_vars(cls)

    @classmethod
    def _name(cls):
        return cls.__name__

    @classmethod
    def __build_vars(cls, obj, strict_format=False):
        _vars = OrderedDict(
            (attr_name, getattr(obj, attr_name))
            for attr_name in dir(obj)
            if not attr_name.startswith('_'))

        for name, value in _vars.copy().items():
            try:
                _vars[name] = cls.__format_value(value, _vars, name)
            except NotImplementedError:
                if strict_format:
                    raise errors.PropertyIsNotImplementedError(
                        'Var "{}" is not implemented in "{}" asset instance',
                        name, obj._name())
                else:
                    del _vars[name]
            except KeyError as e:
                if strict_format:
                    raise errors.ValueSubstitutionError(
                        'Attribute "{}" must be available for "{}" asset instance',
                        e.args[0], obj._name())
                else:
                    del _vars[name]
            except errors.ValueSubstitutionInfiniteLoopError:
                raise errors.ValueSubstitutionInfiniteLoopError(
                    'Attribute "{}" has an infinite string substitution'
                    ' loop for "{}" asset instance',
                    name, obj._name())

        return _vars

    @classmethod
    def __format_value(cls, value, context, start_key):
        if value is NotImplemented:
            raise NotImplementedError
        if isinstance(value, six.string_types):
            for key in cls._string_format_regex.findall(value):
                if key == start_key:
                    raise errors.ValueSubstitutionInfiniteLoopError
                context[key] = cls.__format_value(
                    context[key], context, start_key)
            return value.format(**context)
        if isinstance(value, Mapping):
            return OrderedDict(
                (k, cls.__format_value(v, context, start_key)) for k, v in value.items())
        if isinstance(value, Sequence):
            return [cls.__format_value(v, context, start_key) for v in value]
        return value
