import attr
from ordered_set import OrderedSet

from pyventory.asset import Asset


__all__ = []


@attr.s
class AssetData:
    vars = attr.ib(default=attr.Factory(dict))
    children = attr.ib(default=attr.Factory(OrderedSet))
    instances = attr.ib(default=attr.Factory(OrderedSet))


class Inventory:

    def __init__(self, instances):
        self.assets = {}
        self.instances = {}

        for name, instance in sorted(instances.items()):
            self.add_instance(name, instance)

    def add_instance(self, name, instance):
        if not isinstance(instance, Asset):
            return

        self.instances[name] = instance._vars(instance, strict=True)
        self.add_asset(instance.__class__)
        self.assets[instance._name].instances.add(name)

    def add_asset(self, asset):
        if asset._name in self.assets:
            return

        for parent_asset in asset.__bases__:
            # skip mixins
            if not issubclass(parent_asset, Asset):
                continue
            # skip Asset itself
            if parent_asset is Asset:
                continue

            self.add_asset(parent_asset)
            self.assets[parent_asset._name].children.add(asset._name)

        self.assets[asset._name] = AssetData(vars=asset._vars(asset))
