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

    str_out = StringIO()
    export_inventory(locals(), out=str_out, indent=4)

    assert str_out.getvalue() == '''{
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
