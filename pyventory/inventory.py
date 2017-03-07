import json
import sys

import attr


__all__ = ['Asset', 'export_inventory']


@attr.s
class GroupData:
    hosts = attr.ib(default=attr.Factory(set))
    vars = attr.ib(default=attr.Factory(dict))
    children = attr.ib(default=attr.Factory(set))


class Inventory:
    group_registry = {}

    def __init__(self, hosts):
        self.groups = {}
        self.hosts = {}

        for name, host in hosts.items():
            self.add_host(name, host)

    def add_host(self, name, host):
        self.hosts[name] = host._host_vars

        for group in host.__class__.__bases__:
            group_name = group.__name__

            # skip mixins
            if group_name not in self.group_registry:
                continue

            if group_name not in self.groups:
                self.add_group(group_name)

            self.groups[group_name].hosts.add(name)

    def add_group(self, name):
        if name in self.groups:
            return

        group = self.group_registry[name]
        self.groups[name] = group

        for parent_name in self._get_parent_names(name):
            self.add_group(parent_name)

    def export(self, sort=False):
        data = {
            name: attr.asdict(group) for name, group in self.groups.items()}
        for group in data.values():
            group['children'] = list(
                set(group['children']).intersection(data.keys()))
            if sort:
                group['children'].sort()
            for attr_name in ('hosts', 'vars', 'children',):
                if not group[attr_name]:
                    del group[attr_name]

        data['_meta'] = {'hostvars': self.hosts.copy()}
        return data

    @classmethod
    def register_group(cls, item):
        cls.group_registry[item.__name__] = GroupData(
            vars=item._group_vars())

    @classmethod
    def register_child(cls, item, parent):
        cls.group_registry[parent.__name__].children.add(item.__name__)

    @classmethod
    def _get_parent_names(cls, name):
        parent_names = set()

        for group_name, group in cls.group_registry.items():
            if name in group.children:
                parent_names.add(group_name)

        return parent_names


class AssetMeta(type):

    def __new__(cls, name, bases, attrs):
        item = super().__new__(cls, name, bases, attrs)
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


class Asset(metaclass=AssetMeta):
    __template_vars = None  # typing: list

    def __init__(self, **kwargs):
        var_data = self._group_vars()
        var_data.update(kwargs)
        self._host_vars = var_data

    @classmethod
    def _group_vars(cls):
        return {
            name: value
            for name, value in vars(cls).items()
            if not name.startswith('_')}


def export_inventory(hosts, out=sys.stdout, indent=None, sort=True):
    inventory = Inventory({
        name: obj
        for name, obj in hosts.items()
        if isinstance(obj, Asset)})
    json.dump(
        inventory.export(sort=sort),
        out,
        indent=indent,
        sort_keys=sort)
