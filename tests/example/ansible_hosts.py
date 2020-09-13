#!/usr/bin/env python3
from inventory import assets

from pyventory import ansible_inventory, terraform_vars


ansible_inventory(hosts=vars(assets), indent=4)
