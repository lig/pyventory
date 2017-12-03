import pytest
import six

from pyventory import Asset, ansible_inventory, errors


def test_allow_mixins_for_inventory_items():

    class BaseTestAsset(Asset):
        pass

    class TestMixin(object):
        pass

    class TestAsset(TestMixin, BaseTestAsset):
        pass

    test_asset = TestAsset()

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "BaseTestAsset": {
        "children": [
            "TestAsset"
        ]
    },
    "TestAsset": {
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
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
        "hosts": [
            "test_asset"
        ]
    },
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
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {
                "bar": "ham",
                "foo": "test_ham"
            }
        }
    }
}'''


def test_allow_mapping_of_format_strings_as_values():

    class TestAsset(Asset):
        foo = dict(
            baz='test_{bar}',
        )

    test_asset = TestAsset(bar='ham')

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {
                "bar": "ham",
                "foo": {
                    "baz": "test_ham"
                }
            }
        }
    }
}'''


def test_allow_sequence_of_format_strings_as_values():

    class TestAsset(Asset):
        foo = ['baz', 'test_{bar}']

    test_asset = TestAsset(bar='ham')

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {
                "bar": "ham",
                "foo": [
                    "baz",
                    "test_ham"
                ]
            }
        }
    }
}'''


def test_strings_formatting_do_not_conflict_with_numbers():

    class TestAsset(Asset):
        foo = 42

    test_asset = TestAsset(bar='ham')

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
        "vars": {
            "foo": 42
        },
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {
                "bar": "ham",
                "foo": 42
            }
        }
    }
}'''


def test_require_arguments_for_format_strings():

    class TestAsset(Asset):
        foo = '{bar}'

    test_asset = TestAsset()

    with pytest.raises(errors.ValueSubstitutionError):
        ansible_inventory(locals())


def test_inheritance_with_format():

    class ParentAsset(Asset):
        foo = '{bar}'

    class ChildAsset(ParentAsset):
        pass

    child_asset = ChildAsset(bar='ham')

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "ParentAsset": {
        "children": [
            "ChildAsset"
        ]
    },
    "ChildAsset": {
        "hosts": [
            "child_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "child_asset": {
                "bar": "ham",
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
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "Level1Asset1": {
        "vars": {
            "foo": "Level1Asset1 foo value"
        },
        "children": [
            "Level2Asset3"
        ]
    },
    "Level1Asset2": {
        "vars": {
            "bar": "Level1Asset2 bar value",
            "foo": "Level1Asset2 foo value"
        },
        "children": [
            "Level2Asset3"
        ]
    },
    "Level2Asset3": {
        "vars": {
            "bar": "Level1Asset2 bar value",
            "foo": "Level1Asset1 foo value"
        },
        "children": [
            "Level3Asset4"
        ]
    },
    "Level3Asset4": {
        "vars": {
            "bar": "Level1Asset2 bar value",
            "baz": "Level3Asset4 baz value",
            "foo": "Level1Asset1 foo value"
        },
        "hosts": [
            "level3_asset4"
        ]
    },
    "_meta": {
        "hostvars": {
            "level3_asset4": {
                "bar": "Level1Asset2 bar value",
                "baz": "Level3Asset4 baz value",
                "foo": "Level1Asset1 foo value"
            }
        }
    }
}'''


def test_skip_non_asset_locals():

    class TestAsset(Asset):
        pass

    class TestObject(object):
        pass

    test_asset = TestAsset()
    test_object = TestObject()

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "TestAsset": {
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


def test_multiple_children():

    class BaseTestAsset(Asset):
        pass

    class TestAsset1(BaseTestAsset):
        pass

    class TestAsset2(BaseTestAsset):
        pass

    test_asset1 = TestAsset1()
    test_asset2 = TestAsset2()

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "BaseTestAsset": {
        "children": [
            "TestAsset1",
            "TestAsset2"
        ]
    },
    "TestAsset1": {
        "hosts": [
            "test_asset1"
        ]
    },
    "TestAsset2": {
        "hosts": [
            "test_asset2"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset1": {},
            "test_asset2": {}
        }
    }
}'''


def test_allow_notimplemented_value():

    class BaseTestAsset(Asset):
        foo = NotImplemented

    class TestAsset(BaseTestAsset):
        foo = 'bar'

    test_asset = TestAsset()

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "BaseTestAsset": {
        "children": [
            "TestAsset"
        ]
    },
    "TestAsset": {
        "vars": {
            "foo": "bar"
        },
        "hosts": [
            "test_asset"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset": {
                "foo": "bar"
            }
        }
    }
}'''


def test_raise_notimplemented_value_in_host():

    class BaseTestAsset(Asset):
        foo = NotImplemented

    class TestAsset(BaseTestAsset):
        pass

    test_asset = TestAsset()

    with pytest.raises(errors.PropertyIsNotImplementedError):
        ansible_inventory(locals())


def test_string_format_does_not_miss_values():

    class BaseTestAsset(Asset):
        baz = 'baz-value'

    class TestAsset1(BaseTestAsset):
        bar = '{baz}'
        foo = '{bar}'

    class TestAsset2(BaseTestAsset):
        bar = '{foo}'
        foo = '{baz}'

    test_asset_1 = TestAsset1()
    test_asset_2 = TestAsset2()

    result = six.StringIO()
    ansible_inventory(locals(), out=result, indent=4)

    # hack for py27 `json.dump()` behavior
    result = '\n'.join([x.rstrip() for x in result.getvalue().split('\n')])

    assert result == '''{
    "BaseTestAsset": {
        "vars": {
            "baz": "baz-value"
        },
        "children": [
            "TestAsset1",
            "TestAsset2"
        ]
    },
    "TestAsset1": {
        "vars": {
            "bar": "baz-value",
            "baz": "baz-value",
            "foo": "baz-value"
        },
        "hosts": [
            "test_asset_1"
        ]
    },
    "TestAsset2": {
        "vars": {
            "bar": "baz-value",
            "baz": "baz-value",
            "foo": "baz-value"
        },
        "hosts": [
            "test_asset_2"
        ]
    },
    "_meta": {
        "hostvars": {
            "test_asset_1": {
                "bar": "baz-value",
                "baz": "baz-value",
                "foo": "baz-value"
            },
            "test_asset_2": {
                "bar": "baz-value",
                "baz": "baz-value",
                "foo": "baz-value"
            }
        }
    }
}''', result


def test_string_format_detects_infinite_loop():

    class TestAsset(Asset):
        bar = '{foo}'
        foo = '{bar}'

    test_asset = TestAsset()

    with pytest.raises(errors.ValueSubstitutionInfiniteLoopError):
        ansible_inventory(locals())
