from io import StringIO

import pytest

from pyventory import Asset, export_inventory


def test_allow_mixins_for_inventory_items():

    class BaseTestAsset(Asset):
        pass

    class TestMixin:
        pass

    class TestAsset(TestMixin, BaseTestAsset):
        pass

    test_asset = TestAsset()

    result = StringIO()
    export_inventory(locals(), out=result, indent=4)

    assert result.getvalue() == '''{
    "BaseTestAsset": {
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {}
        }
    }
}'''


def test_allow_host_specific_vars():

    class TestAsset(Asset):
        pass

    test_asset = TestAsset(foo='bar')

    result = StringIO()
    export_inventory(locals(), out=result, indent=4)

    assert result.getvalue() == '''{
    "_meta": {
        "hostvars": {
            "test_asset": {
                "foo": "bar"
            }
        }
    }
}'''


def test_allow_format_strings_as_values():

    class TestAsset(Asset):
        foo = 'test_{bar}'

    test_asset = TestAsset(bar='ham')

    result = StringIO()
    export_inventory(locals(), out=result, indent=4)

    assert result.getvalue() == '''{
    "_meta": {
        "hostvars": {
            "test_asset": {
                "foo": "test_ham"
            }
        }
    }
}'''


def test_require_arguments_for_format_strings():

    class TestAsset(Asset):
        foo = '{bar}'

    with pytest.raises(ValueError):
        TestAsset()
