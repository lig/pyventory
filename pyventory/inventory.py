from collections import OrderedDict

from ordered_set import OrderedSet
import attr

from pyventory.asset import Asset


__all__ = []


@attr.s
class GroupData(object):
    vars = attr.ib(default=attr.Factory(OrderedDict))
    children = attr.ib(default=attr.Factory(OrderedSet))
    hosts = attr.ib(default=attr.Factory(OrderedSet))


class Inventory(object):

    def __init__(self, hosts):
        self.groups = OrderedDict()
        self.hosts = OrderedDict()

        for name, host in sorted(hosts.items()):
            self.add_host(name, host)

    def add_host(self, name, host):
        if not isinstance(host, Asset):
            return

        self.hosts[name] = host._vars()
        self.add_group(host.__class__)
        self.groups[host._name()].hosts.add(name)

    def add_group(self, asset):
        if asset._name() in self.groups:
            return

        for parent_asset in asset.__bases__:
            # skip mixins
            if not issubclass(parent_asset, Asset):
                continue
            # skip Asset itself and object
            if parent_asset in (Asset, object,):
                continue

            self.add_group(parent_asset)
            self.groups[parent_asset._name()].children.add(asset._name())

        self.groups[asset._name()] = GroupData(vars=asset._cls_vars())
