#!/usr/bin/env python
import pathlib

from inventory import assets

from pyventory import terraform_vars


terraform_vars(
    instances=vars(assets),
    filename_base=pathlib.Path(__file__).parent / 'terraform_result',
    indent=4)
