#!/usr/bin/env python
from pyventory import ansible_inventory, terraform_vars

from inventory import assets


ansible_inventory(vars(assets), indent=4)
