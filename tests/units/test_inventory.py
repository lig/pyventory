from pyventory import InventoryItem, export_inventory
from io import StringIO


def test_allow_mixins_for_inventory_items():

    class BaseTestItem(InventoryItem):
        pass

    class TestMixin:
        pass

    class TestItem(TestMixin, BaseTestItem):
        pass

    test_item = TestItem()

    str_out = StringIO()
    export_inventory(locals(), out=str_out, indent=4)

    assert str_out.getvalue() == '''{
    "BaseTestItem": {
        "hosts": [
            "test_item"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_item": {}
        }
    }
}'''
