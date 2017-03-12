import attr

from pyventory.registry import AssetData, Registry


__all__ = []


@attr.s
class GroupData(AssetData):
    hosts = attr.ib(default=attr.Factory(set))


class Inventory(object):

    def __init__(self, hosts):
        self.groups = {}
        self.hosts = {}

        for name, host in hosts.items():
            self.add_host(name, host)

    def add_host(self, name, host):
        self.hosts[name] = host._host_vars

        for asset in host.__class__.__bases__:
            asset_name = asset.__name__

            # skip mixins
            if not Registry.is_registered(asset_name):
                continue

            if asset_name not in self.groups:
                self.add_group(asset_name)

            self.groups[asset_name].hosts.add(name)

    def add_group(self, name):
        if name in self.groups:
            return

        self.groups[name] = GroupData(**attr.asdict(Registry.get_asset(name)))

        for parent_name in Registry.get_parent_names(name):
            self.add_group(parent_name)

    def export(self, sort=False):
        data = {
            name: attr.asdict(group) for name, group in self.groups.items()}
        for group in data.values():
            group['children'] = list(
                set(group['children']).intersection(data.keys()))
            if sort:
                group['hosts'].sort()
                group['children'].sort()
            for attr_name in ('hosts', 'vars', 'children',):
                if not group[attr_name]:
                    del group[attr_name]

        data['_meta'] = {'hostvars': self.hosts.copy()}
        return data
