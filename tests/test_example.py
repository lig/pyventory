import json
import os
import shlex
import subprocess

import pytest


@pytest.fixture(scope='session')
def example_dir(tests_dir):
    return tests_dir / 'example'


@pytest.fixture(scope='session')
def anisble_inventory(example_dir):
    return open(str(example_dir / 'ansible.json'), 'r')


@pytest.fixture(scope='session')
def terraform_config(example_dir):
    return open(str(example_dir / 'terraform.tf'), 'r')


def test_ansible_inventory(tests_dir, example_dir, anisble_inventory):
    project_dir = tests_dir.parent
    inventory_exe = example_dir / 'ansible_hosts.py'

    result = subprocess.check_output(
        shlex.split(str(inventory_exe)),
        env=dict(
            os.environ,
            PYTHONPATH='{}:{}'.format(project_dir, example_dir)))

    assert json.loads(result.decode()) == json.load(anisble_inventory)


def test_terraform_vars(tests_dir, example_dir, terraform_config):
    project_dir = tests_dir.parent
    inventory_exe = example_dir / 'terraform_vars.py'

    subprocess.check_call(
        shlex.split(str(inventory_exe)),
        env=dict(
            os.environ,
            PYTHONPATH='{}:{}'.format(project_dir, example_dir)))

    result_path = example_dir / 'terraform_result.tf'
    result = open(str(result_path), 'r')

    assert json.load(result) == json.load(terraform_config)

    result_path.unlink()
