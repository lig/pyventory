from pathlib import Path
import os
import shlex
import subprocess


def test_example_inventory():
    project_dir = Path(__file__).parents[2].absolute()
    example_dir = project_dir.joinpath('tests', 'e2e', 'example')
    inventory_exe = example_dir.joinpath('hosts.py')

    result = subprocess.run(
        shlex.split(str(inventory_exe)),
        stdout=subprocess.PIPE,
        env=dict(
            os.environ,
            PYTHONPATH='{}:{}'.format(project_dir, example_dir)))

    assert result.stdout == b''
