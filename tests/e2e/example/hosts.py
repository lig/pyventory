#!/usr/bin/env python
from pyventory import export_inventory

from pyvars import *


develop = DevelopHost()
develop_sidebranch = DevelopHost(
    ansible_host='sidebranch_hostname',
    version='sidebranch_name')

staging = StagingHost()

prod_backend1 = ProdBackEnd(num=1)
prod_backend2 = ProdBackEnd(num=2)
prod_frontend1 = ProdFrontEnd(num=1)
prod_frontend2 = ProdFrontEnd(num=2)

export_inventory(locals(), indent=4)
