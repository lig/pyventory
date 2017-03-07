from pyventory import Asset, export_inventory
from io import StringIO


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
