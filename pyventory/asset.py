import string

import six

from pyventory.inventory import Inventory


__all__ = ['Asset']


class AssetMeta(type):

    def __new__(cls, name, bases, attrs):
        item = super(AssetMeta, cls).__new__(cls, name, bases, attrs)
        if not bases:
            return item

        Inventory.register_group(item)

        for base in bases:
            if not issubclass(base, Asset):
                continue
            if base is Asset:
                continue
            Inventory.register_child(item, base)

        return item


class Asset(six.with_metaclass(AssetMeta)):

    def __init__(self, **kwargs):
        var_data = self._group_vars()

        for template_name, template_vars in self._template_map().items():
            try:
                template_data = {var: kwargs.pop(var) for var in template_vars}
            except KeyError:
                raise ValueError(
                    'Not enough arguments for template `%s`: "%s"',
                    template_name,
                    var_data[template_name])

            var_data[template_name] = var_data[template_name].format(
                **template_data)

        var_data.update(kwargs)
        self._host_vars = var_data

    @classmethod
    def _group_vars(cls):
        return {
            name: value
            for name, value in vars(cls).items()
            if not name.startswith('_')}

    @classmethod
    def _template_map(cls):
        formatter = string.Formatter()
        template_map = {}

        for name, value in cls._group_vars().items():
            template_vars = [
                chunk[1]
                for chunk in formatter.parse(value)
                if chunk[1] is not None]

            if not template_vars:
                continue

            template_map[name] = template_vars

        return template_map
