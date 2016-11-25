from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def tests_dir():
    return Path(__file__).parent.absolute()
