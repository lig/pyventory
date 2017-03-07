import os
import shlex
import subprocess

import pytest


@pytest.fixture(scope='session')
def example_inventory(tests_dir):
    return open(str(tests_dir.joinpath('e2e', 'example.json')), 'r').read()


def test_example_inventory(tests_dir, example_inventory):
    project_dir = tests_dir.parent
    example_dir = tests_dir.joinpath('e2e', 'example')
    inventory_exe = example_dir.joinpath('hosts.py')

    result = subprocess.check_output(
        shlex.split(str(inventory_exe)),
        env=dict(
            os.environ,
            PYTHONPATH='{}:{}'.format(project_dir, example_dir)))

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.decode().split('\n')])

    assert result == example_inventory
