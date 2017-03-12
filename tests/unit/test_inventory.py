import pytest
import six

from pyventory import Asset, export_inventory


def test_allow_mixins_for_inventory_items():

    class BaseTestAsset(Asset):
        pass

    class TestMixin(object):
        pass

    class TestAsset(TestMixin, BaseTestAsset):
        pass

    test_asset = TestAsset()

    result = six.StringIO()
    export_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
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

    result = six.StringIO()
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

    result = six.StringIO()
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


def test_inheritance_with_format():

    class ParentAsset(Asset):
        foo = '{bar}'

    class ChildAsset(ParentAsset):
        pass

    child_asset = ChildAsset(bar='ham')

    result = six.StringIO()
    export_inventory(locals(), out=result, indent=4)

    assert result.getvalue() == '''{
    "ParentAsset": {
        "hosts": [
            "child_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "child_asset": {
                "foo": "ham"
            }
        }
    }
}'''


def test_deep_multiple_inheritance_propagation():

    class Level1Asset1(Asset):
        foo = 'Level1Asset1 foo value'

    class Level1Asset2(Asset):
        foo = 'Level1Asset2 foo value'
        bar = 'Level1Asset2 bar value'

    class Level2Asset3(Level1Asset1, Level1Asset2):
        pass

    class Level3Asset4(Level2Asset3):
        baz = 'Level3Asset4 baz value'

    level3_asset4 = Level3Asset4()

    result = six.StringIO()
    export_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "Level1Asset1": {
        "children": [
            "Level2Asset3"
        ],
        "vars": {
            "foo": "Level1Asset1 foo value"
        }
    },
    "Level1Asset2": {
        "children": [
            "Level2Asset3"
        ],
        "vars": {
            "bar": "Level1Asset2 bar value",
            "foo": "Level1Asset2 foo value"
        }
    },
    "Level2Asset3": {
        "hosts": [
            "level3_asset4"
        ],
        "vars": {
            "foo": "Level1Asset1 foo value"
            "bar": "Level1Asset2 bar value",
        }
    },
    "_meta": {
        "hostvars": {
            "level3_asset4": {
                "foo": "Level1Asset1 foo value"
                "bar": "Level1Asset2 bar value",
                "baz": "Level3Asset4 baz value"
            }
        }
    }
}'''
