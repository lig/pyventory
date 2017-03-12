import json
import sys

from pyventory.asset import Asset
from pyventory.inventory import Inventory


__all__ = ['export_inventory']


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
