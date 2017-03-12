import attr


__all__ = []


@attr.s
class AssetData(object):
    vars = attr.ib(default=attr.Factory(dict))
    children = attr.ib(default=attr.Factory(set))


class Registry(object):
    registry = {}

    @classmethod
    def register_asset(cls, item):
        cls.registry[item.__name__] = AssetData(vars=item._asset_vars())

    @classmethod
    def register_child(cls, item, parent):
        cls.registry[parent.__name__].children.add(item.__name__)

    @classmethod
    def is_registered(cls, asset_name):
        return asset_name in cls.registry

    @classmethod
    def get_asset(cls, asset_name):
        return cls.registry[asset_name]

    @classmethod
    def get_parent_names(cls, child_name):
        parent_names = set()

        for asset_name, asset in cls.registry.items():
            if child_name in asset.children:
                parent_names.add(asset_name)

        return parent_names
