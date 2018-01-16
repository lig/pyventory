import json
import sys
from collections import OrderedDict

import attr

from pyventory.inventory import Inventory


__all__ = ['pyventory_data', 'ansible_inventory']


def pyventory_data(hosts):
    """Provides raw inventory data as Python `dict` containing Asset data in
    `assets` key and hosts data in `hosts` key.
    """
    inventory = Inventory(hosts)

    assets = OrderedDict(
        (name, attr.asdict(asset, dict_factory=OrderedDict))
        for name, asset in inventory.assets.items())

    for asset in assets.values():
        for attr_name in ('hosts', 'vars', 'children',):
            if not asset[attr_name]:
                del asset[attr_name]

    hosts = inventory.hosts.copy()

    return {'assets': assets, 'hosts': hosts}


def ansible_inventory(hosts, out=sys.stdout, indent=None):
    """Dumps inventory in the Ansible's Dynamic Inventory JSON format to `out`.
    """
    raw_data = pyventory_data(hosts)

    data = OrderedDict(raw_data['assets'])
    data['_meta'] = {'hostvars': raw_data['hosts']}

    json.dump(data, out, indent=indent, default=list)
