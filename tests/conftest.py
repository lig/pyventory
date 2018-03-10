import pathlib

import pytest


@pytest.fixture(scope='session')
def tests_dir():
    return pathlib.Path(__file__).parent.absolute()
