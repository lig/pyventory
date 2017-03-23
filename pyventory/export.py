from collections import OrderedDict
import json
import sys

import attr

from pyventory.inventory import Inventory


__all__ = ['ansible_inventory']


def ansible_inventory(hosts, out=sys.stdout, indent=None):
    inventory = Inventory(hosts)

    data = OrderedDict(
        (name, attr.asdict(group, dict_factory=OrderedDict))
        for name, group in inventory.groups.items())

    for group in data.values():
        for attr_name in ('hosts', 'vars', 'children',):
            if not group[attr_name]:
                del group[attr_name]

    data['_meta'] = {'hostvars': inventory.hosts.copy()}

    json.dump(data, out, indent=indent, default=list)
