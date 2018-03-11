#!/usr/bin/env python3
from pyventory import ansible_inventory, terraform_vars

from inventory import assets


ansible_inventory(hosts=vars(assets), indent=4)
