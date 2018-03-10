import json
import pathlib
import sys
from collections import Mapping, Sequence

import attr

from pyventory.inventory import Inventory


__all__ = ['pyventory_data', 'ansible_inventory', 'terraform_vars']


def pyventory_data(hosts):
    """Provides raw inventory data as Python `dict` containing Asset data in
    `assets` key and hosts data in `hosts` key.
    """
    inventory = Inventory(hosts)

    assets = {
        name: attr.asdict(asset)
        for name, asset in inventory.assets.items()}

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

    data = raw_data['assets']
    data['_meta'] = {'hostvars': raw_data['hosts']}

    json.dump(data, out, indent=indent, default=list)


def terraform_vars(hosts, filename_base='pyventory', indent=None):
    """Dumps inventory in the Terraform's JSON format to `<filename_base>.tf`
    setting their values as defaults.
    """
    tf_config_path = pathlib.Path(filename_base).with_suffix('.tf')

    raw_data = pyventory_data(hosts)

    tf_config = {}

    for asset_name, asset_data in raw_data['hosts'].items():

        for name, value in asset_data.items():

            var_name = f'{asset_name}__{name}'

            var_type = 'string'
            var_value = value

            if isinstance(value, str):
                pass
            elif isinstance(value, bool):
                var_value = str(value).lower()
            elif isinstance(value, (int, float,)):
                var_value = str(value)
            elif isinstance(value, Mapping):
                var_type = 'map'
            elif isinstance(value, Sequence):
                var_type = 'list'

            tf_config[var_name] = {
                'type': var_type,
                'default': var_value,
            }

    tf_config = {'variable': tf_config}

    json.dump(tf_config, open(tf_config_path, 'w'), indent=indent)
