import re
import types
import typing
from collections import abc

from pyventory import errors


__all__ = ['Asset']


AssetObj_T = typing.Union['Asset', typing.Type['Asset']]
AttrValueFinal_T = typing.Union[str, int, float, typing.Iterable, typing.Mapping]
AttrValueDef_T = typing.Union[types.NotImplementedType, AttrValueFinal_T]
AssetContext_T = typing.Dict[str, AttrValueDef_T]


class SKIP_ATTR:
    pass


class AssetAttr:
    _value: AttrValueDef_T
    _name: str

    def __init__(self, value: AttrValueDef_T) -> None:
        self._value = value

    def __get__(
        self, instance: typing.Optional['Asset'], owner: typing.Type['Asset']
    ) -> AttrValueDef_T:
        if instance is not None:
            return self._value

        if not isinstance(self._value, (str, abc.Mapping, abc.Sequence)):
            return self._value

        def get_attr() -> AttrValueFinal_T:
            return typing.cast(
                AttrValueFinal_T, owner._get_attr(owner, self._name, strict=True)
            )

        value_type = type(self._value)
        return type(
            value_type.__name__, (value_type,), {'__call__': staticmethod(get_attr)}
        )(self._value)

    def __set_name__(self, owner: typing.Type['Asset'], name: str) -> None:
        self._name = name


class AssetMeta(type):
    def __new__(
        cls,
        name: str,
        bases: typing.Tuple[typing.Type, ...],
        namespace: typing.Dict[str, typing.Any],
        **kwds: typing.Any,
    ) -> 'AssetMeta':
        new_namespace = {
            '_name': f'{namespace["__module__"]}.{name}',
        }

        for key, value in namespace.items():
            if not key.startswith('_'):
                value = AssetAttr(value)
            new_namespace[key] = value

        return typing.cast(
            'AssetMeta', super().__new__(cls, name, bases, new_namespace)
        )


class Asset(metaclass=AssetMeta):
    _name: typing.ClassVar[str]

    _string_format_regex = re.compile(r'(?<!{){([\w_]+)}(?!<})')

    def __new__(cls, **kwargs: AttrValueFinal_T) -> 'Asset':
        self = super().__new__(cls)
        self.__dict__.update(kwargs)
        self.__dict__.update(self._vars(self, strict=True))
        return self

    @staticmethod
    def _attrs(obj: AssetObj_T) -> typing.Iterable[str]:
        return [name for name in dir(obj) if not name.startswith('_')]

    @staticmethod
    def _context(obj: AssetObj_T) -> AssetContext_T:
        return {name: getattr(obj, name) for name in obj._attrs(obj)}

    @staticmethod
    def _vars(
        obj: AssetObj_T, strict: bool = False
    ) -> typing.Mapping[str, AttrValueFinal_T]:
        return {
            name: typing.cast(AttrValueFinal_T, value)
            for name, value in (
                (name, obj._get_attr(obj, name, strict=strict))
                for name in obj._attrs(obj)
            )
            if value is not SKIP_ATTR
        }

    @staticmethod
    def _get_attr(
        obj: AssetObj_T, name: str, strict: bool = False
    ) -> typing.Union[AttrValueFinal_T, typing.Type[SKIP_ATTR]]:
        try:
            context = obj._context(obj).copy()
            return obj._format_value(obj, context, context[name], name)
        except NotImplementedError:
            if strict:
                raise errors.PropertyIsNotImplementedError(
                    f'Var "{name}" is not implemented in "{obj._name}" asset'
                )
            else:
                return SKIP_ATTR
        except KeyError as e:
            if strict:
                raise errors.ValueSubstitutionError(
                    f'Attribute "{e.args[0]}" must be available for'
                    f' "{obj._name}" asset instance'
                )
            else:
                return SKIP_ATTR
        except errors.ValueSubstitutionInfiniteLoopError:
            raise errors.ValueSubstitutionInfiniteLoopError(
                f'Attribute "{name}" has an infinite string substitution'
                f' loop in "{obj._name}" asset instance'
            )

    @staticmethod
    def _format_value(
        obj: AssetObj_T, context: AssetContext_T, value: AttrValueDef_T, start_key: str
    ) -> AttrValueFinal_T:
        if value is NotImplemented:
            raise NotImplementedError
        if isinstance(value, str):
            for key in obj._string_format_regex.findall(value):
                if key == start_key:
                    raise errors.ValueSubstitutionInfiniteLoopError
                context[key] = obj._format_value(obj, context, context[key], start_key)
            return value.format(**context)
        if isinstance(value, abc.Mapping):
            return {
                k: obj._format_value(obj, context, v, start_key)
                for k, v in value.items()
            }
        if isinstance(value, abc.Iterable):
            return [obj._format_value(obj, context, v, start_key) for v in value]
        return value
