import pytest

from pyventory import Asset, errors, pyventory_data


def test_allow_mixins_for_inventory_items():

    class BaseTestAsset(Asset):
        pass

    class TestMixin:
        pass

    class TestAsset(TestMixin, BaseTestAsset):
        pass

    test_asset = TestAsset()

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.BaseTestAsset": {
                "children": [
                    "test_inventory.TestAsset"
                ],
            },
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset",
                ],
            },
        },
        "instances": {
            "test_asset": {}
        },
    }


def test_allow_host_specific_vars():

    class TestAsset(Asset):
        pass

    test_asset = TestAsset(foo='bar')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset",
                ],
            },
        },
        "instances": {
            "test_asset": {
                "foo": "bar"
            },
        },
    }


def test_allow_format_strings_as_values():

    class TestAsset(Asset):
        foo = 'test_{bar}'

    test_asset = TestAsset(bar='ham')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {
                "bar": "ham",
                "foo": "test_ham"
            }
        }
    }


def test_allow_mapping_of_format_strings_as_values():

    class TestAsset(Asset):
        foo = dict(
            baz='test_{bar}',
        )

    test_asset = TestAsset(bar='ham')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {
                "bar": "ham",
                "foo": {
                    "baz": "test_ham"
                }
            }
        }
    }


def test_allow_sequence_of_format_strings_as_values():

    class TestAsset(Asset):
        foo = ['baz', 'test_{bar}']

    test_asset = TestAsset(bar='ham')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {
                "bar": "ham",
                "foo": [
                    "baz",
                    "test_ham"
                ]
            }
        }
    }


def test_strings_formatting_do_not_conflict_with_numbers():

    class TestAsset(Asset):
        foo = 42

    test_asset = TestAsset(bar='ham')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "vars": {
                    "foo": 42
                },
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {
                "bar": "ham",
                "foo": 42
            }
        }
    }


def test_require_arguments_for_format_strings():

    class TestAsset(Asset):
        foo = '{bar}'

    with pytest.raises(errors.ValueSubstitutionError):
        test_asset = TestAsset()


def test_inheritance_with_format():

    class ParentAsset(Asset):
        foo = '{bar}'

    class ChildAsset(ParentAsset):
        pass

    child_asset = ChildAsset(bar='ham')

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.ParentAsset": {
                "children": [
                    "test_inventory.ChildAsset"
                ]
            },
            "test_inventory.ChildAsset": {
                "instances": [
                    "child_asset"
                ]
            },
        },
        "instances": {
            "child_asset": {
                "bar": "ham",
                "foo": "ham"
            }
        }
    }


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

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.Level1Asset1": {
                "vars": {
                    "foo": "Level1Asset1 foo value"
                },
                "children": [
                    "test_inventory.Level2Asset3"
                ]
            },
            "test_inventory.Level1Asset2": {
                "vars": {
                    "bar": "Level1Asset2 bar value",
                    "foo": "Level1Asset2 foo value"
                },
                "children": [
                    "test_inventory.Level2Asset3"
                ]
            },
            "test_inventory.Level2Asset3": {
                "vars": {
                    "bar": "Level1Asset2 bar value",
                    "foo": "Level1Asset1 foo value"
                },
                "children": [
                    "test_inventory.Level3Asset4"
                ]
            },
            "test_inventory.Level3Asset4": {
                "vars": {
                    "bar": "Level1Asset2 bar value",
                    "baz": "Level3Asset4 baz value",
                    "foo": "Level1Asset1 foo value"
                },
                "instances": [
                    "level3_asset4"
                ]
            },
        },
        "instances": {
            "level3_asset4": {
                "bar": "Level1Asset2 bar value",
                "baz": "Level3Asset4 baz value",
                "foo": "Level1Asset1 foo value"
            }
        }
    }


def test_skip_non_asset_locals():

    class TestAsset(Asset):
        pass

    class TestObject:
        pass

    test_asset = TestAsset()
    test_object = TestObject()

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.TestAsset": {
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {}
        }
    }


def test_multiple_children():

    class BaseTestAsset(Asset):
        pass

    class TestAsset1(BaseTestAsset):
        pass

    class TestAsset2(BaseTestAsset):
        pass

    test_asset1 = TestAsset1()
    test_asset2 = TestAsset2()

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.BaseTestAsset": {
                "children": [
                    "test_inventory.TestAsset1",
                    "test_inventory.TestAsset2"
                ]
            },
            "test_inventory.TestAsset1": {
                "instances": [
                    "test_asset1"
                ]
            },
            "test_inventory.TestAsset2": {
                "instances": [
                    "test_asset2"
                ]
            },
        },
        "instances": {
            "test_asset1": {},
            "test_asset2": {}
        }
    }


def test_allow_notimplemented_value():

    class BaseTestAsset(Asset):
        foo = NotImplemented

    class TestAsset(BaseTestAsset):
        foo = 'bar'

    test_asset = TestAsset()

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.BaseTestAsset": {
                "children": [
                    "test_inventory.TestAsset"
                ]
            },
            "test_inventory.TestAsset": {
                "vars": {
                    "foo": "bar"
                },
                "instances": [
                    "test_asset"
                ]
            },
        },
        "instances": {
            "test_asset": {
                "foo": "bar"
            }
        }
    }


def test_raise_notimplemented_value_in_final_asset():

    class BaseTestAsset(Asset):
        foo = NotImplemented

    class TestAsset(BaseTestAsset):
        pass

    with pytest.raises(errors.PropertyIsNotImplementedError):
        test_asset = TestAsset()


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

    result = pyventory_data(locals())

    assert result == {
        'assets': {
            "test_inventory.BaseTestAsset": {
                "vars": {
                    "baz": "baz-value"
                },
                "children": [
                    "test_inventory.TestAsset1",
                    "test_inventory.TestAsset2"
                ]
            },
            "test_inventory.TestAsset1": {
                "vars": {
                    "bar": "baz-value",
                    "baz": "baz-value",
                    "foo": "baz-value"
                },
                "instances": [
                    "test_asset_1"
                ]
            },
            "test_inventory.TestAsset2": {
                "vars": {
                    "bar": "baz-value",
                    "baz": "baz-value",
                    "foo": "baz-value"
                },
                "instances": [
                    "test_asset_2"
                ]
            },
        },
        "instances": {
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


def test_string_format_detects_infinite_loop():

    class TestAsset(Asset):
        bar = '{foo}'
        foo = '{bar}'

    with pytest.raises(errors.ValueSubstitutionInfiniteLoopError):
        test_asset = TestAsset()
