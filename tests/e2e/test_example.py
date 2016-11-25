import os
import shlex
import subprocess

import pytest


@pytest.fixture(scope='session')
def example_inventory(tests_dir):
    return open(str(tests_dir.joinpath('e2e', 'example.json')), 'rb').read()


def test_example_inventory(tests_dir, example_inventory):
    project_dir = tests_dir.parent
    example_dir = tests_dir.joinpath('e2e', 'example')
    inventory_exe = example_dir.joinpath('hosts.py')

    result = subprocess.run(
        shlex.split(str(inventory_exe)),
        stdout=subprocess.PIPE,
        env=dict(
            os.environ,
            PYTHONPATH='{}:{}'.format(project_dir, example_dir)))

    assert result.stdout == example_inventory
