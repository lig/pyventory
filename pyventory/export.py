import json
import pathlib
import sys
from collections import Mapping, Sequence

import attr

from pyventory.inventory import Inventory


__all__ = ['pyventory_data', 'ansible_inventory', 'terraform_vars']


def pyventory_data(instances):
    """Provides raw inventory data as Python `dict` containing Asset data in
    `assets` key and instances data in `instances` key.
    """
    inventory = Inventory(instances)

    assets = {
        name: attr.asdict(asset)
        for name, asset in inventory.assets.items()}

    for asset in assets.values():
        for attr_name in ('instances', 'vars', 'children',):
            if not asset[attr_name]:
                del asset[attr_name]

    instances = inventory.instances.copy()

    return {'assets': assets, 'instances': instances}


def ansible_inventory(hosts, out=sys.stdout, indent=None):
    """Dumps inventory in the Ansible's Dynamic Inventory JSON format to `out`.
    """
    raw_data = pyventory_data(hosts)

    data = {}

    for key, value in raw_data['assets'].items():
        if 'instances' in value:
            value['hosts'] = value.pop('instances')
        data[key] = value

    data['_meta'] = {'hostvars': raw_data['instances']}

    json.dump(data, out, indent=indent, default=list)


def terraform_vars(instances, filename_base='pyventory', indent=None):
    """Dumps inventory in the Terraform's JSON format to `<filename_base>.tf`
    setting their values as defaults.
    """
    tf_config_path = pathlib.Path(filename_base).with_suffix('.tf.json')

    raw_data = pyventory_data(instances)

    tf_config = {}

    for asset_name, asset_data in raw_data['instances'].items():

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
                if value and isinstance(value[0], Mapping):
                    var_type = 'map'
                else:
                    var_type = 'list'

            tf_config[var_name] = {
                'type': var_type,
                'default': var_value,
            }

    tf_config = {'variable': tf_config}

    json.dump(tf_config, open(tf_config_path, 'w'), indent=indent)
