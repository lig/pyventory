from pyventory.cli import main


def test_cli_fake():
    assert main() is None
