# Pyventory
Ansible Inventory implementation that uses Python syntax

## Install

```shell
pip install pyventory
```   

## Features
  
* Modular inventory.
* Assests inheritance using Python classes.
* Support for multiple inheritance.
* Support for mixins.
* Support for vars templating using [Python string formatting](https://docs.python.org/3/library/string.html#format-specification-mini-language).
* Python 3 support.
* Python 2 (2.7) support.


## Usage

Create `hosts.py` and make it executable.

A short example of the `hosts.py` contents:

```python
#!/usr/bin/env python
from pyventory import Asset, export_inventory

class All(Asset):
    run_tests = False
    use_redis = False
    redis_host = 'localhost'
    minify = False
    version = 'develop'

class Staging(All):
    run_tests = True

staging = Staging()

export_inventory(locals())
```

Consider a [more complex example](tests/e2e/example) which passes the following [json output](tests/e2e/example.json) to Ansible.

Run Ansible playbook with the `-i hosts.py` key:

```shell
ansible-playbook -i hosts.py site.yml
```

Notice that you need to have your inventory package in `PYTHONPATH`.
