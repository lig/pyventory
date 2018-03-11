import re
from collections import Mapping, Sequence

from pyventory import errors


__all__ = ['Asset']


class SKIP_ATTR:
    pass


class AssetAttr:
    _value = None
    _name = None

    def __init__(self, value):
        self._value = value

    def __get__(self, instance, owner):
        if instance:
            return self._value

        if not isinstance(self._value, (str, Mapping, Sequence)):
            return self._value

        def get_attr(value):
            return owner._get_attr(owner, self._name, strict=True)

        value_type = type(self._value)
        return type(
            value_type.__name__,
            (value_type,),
            {'__call__': get_attr}
        )(self._value)

    def __set_name__(self, owner, name):
        self._name = name


class AssetMeta(type):

    def __new__(cls, name, bases, namespace, **kwds):
        new_namespace = {
            '_name': f'{namespace["__module__"]}.{name}',
        }

        for key, value in namespace.items():
            if not key.startswith('_'):
                value = AssetAttr(value)
            new_namespace[key] = value

        return super().__new__(cls, name, bases, new_namespace, **kwds)


class Asset(metaclass=AssetMeta):

    _string_format_regex = re.compile(r'{([\w_]+)}')

    def __new__(cls, **kwargs):
        self = super().__new__(cls)
        self.__dict__.update(kwargs)
        self.__dict__.update(self._vars(self, strict=True))
        return self

    @staticmethod
    def _attrs(obj):
        return [name for name in dir(obj) if not name.startswith('_')]

    @staticmethod
    def _context(obj):
        return {name: getattr(obj, name) for name in obj._attrs(obj)}

    @staticmethod
    def _vars(obj, strict=False):
        return {
            name: value
            for name, value in (
                (name, obj._get_attr(obj, name, strict=strict))
                for name in obj._attrs(obj))
            if value is not SKIP_ATTR}

    @staticmethod
    def _get_attr(obj, name, strict=False):
        try:
            context = obj._context(obj).copy()
            return obj._format_value(obj, context, context[name], name)
        except NotImplementedError:
            if strict:
                raise errors.PropertyIsNotImplementedError(
                    f'Var "{name}" is not implemented in "{obj._name}" asset')
            else:
                return SKIP_ATTR
        except KeyError as e:
            if strict:
                raise errors.ValueSubstitutionError(
                    f'Attribute "{e.args[0]}" must be available for'
                    f' "{obj._name}" asset instance')
            else:
                return SKIP_ATTR
        except errors.ValueSubstitutionInfiniteLoopError:
            raise errors.ValueSubstitutionInfiniteLoopError(
                f'Attribute "{name}" has an infinite string substitution'
                f' loop in "{obj._name}" asset instance')

    @staticmethod
    def _format_value(obj, context, value, start_key):
        if value is NotImplemented:
            raise NotImplementedError
        if isinstance(value, str):
            for key in obj._string_format_regex.findall(value):
                if key == start_key:
                    raise errors.ValueSubstitutionInfiniteLoopError
                context[key] = obj._format_value(
                    obj, context, context[key], start_key)
            return value.format(**context)
        if isinstance(value, Mapping):
            return {
                k: obj._format_value(obj, context, v, start_key)
                for k, v in value.items()}
        if isinstance(value, Sequence):
            return [
                obj._format_value(obj, context, v, start_key) for v in value]
        return value
