import typing
from collections import abc

import attr
from ordered_set import OrderedSet

from . import assets


MaybeAsset_T = typing.Union[assets.Asset, typing.Any]


@attr.s(auto_attribs=True, kw_only=True)
class AssetData:
    vars: typing.Mapping[str, assets.AttrValueFinal_T] = attr.ib(
        default=attr.Factory(dict)
    )
    children: typing.MutableSet[str] = attr.ib(default=attr.Factory(OrderedSet))
    instances: typing.Set[str] = attr.ib(default=attr.Factory(OrderedSet))


class Inventory:
    def __init__(self, instances: typing.Mapping[str, MaybeAsset_T]):
        self.assets: typing.MutableMapping[str, AssetData] = {}
        self.instances: typing.Dict[
            str, typing.Mapping[str, assets.AttrValueFinal_T]
        ] = {}

        for name, instance in sorted(instances.items()):
            self.add_instance(name, instance)

    def add_instance(self, name: str, instance: MaybeAsset_T) -> None:
        if isinstance(instance, abc.Iterable) and not isinstance(instance, str):
            for n, item in enumerate(instance, start=1):
                self.add_instance(name=f'{name}_{n}', instance=item)
            return

        if not isinstance(instance, assets.Asset):
            return

        self.instances[name] = instance._context(instance)
        self.add_asset(instance.__class__)
        self.assets[instance._name].instances.add(name)

    def add_asset(self, asset: typing.Type[assets.Asset]) -> None:
        if asset._name in self.assets:
            return

        for parent_asset in asset.__bases__:
            # skip mixins
            if not issubclass(parent_asset, assets.Asset):
                continue
            # skip Asset itself
            if parent_asset is assets.Asset:
                continue

            self.add_asset(parent_asset)
            self.assets[parent_asset._name].children.add(asset._name)

        self.assets[asset._name] = AssetData(vars=asset._vars(asset))
