import pytest

from pyventory import Asset, errors


def test_calculate_asset_class_attribute_value_on_call():
    class TestAsset(Asset):
        foo = '{bar}'
        bar = 'bar'

    assert TestAsset.foo() == 'bar'


def test_escaped_braces_do_not_act_as_a_value_template_in_attr():
    class TestAsset(Asset):
        foo = '{{bar}}'

    assert TestAsset.foo() == '{bar}'


def test_use_raw_asset_class_attribute_value():
    class TestAsset(Asset):
        foo = '{bar}-{baz}'
        bar = 'bar'

    assert TestAsset.foo == '{bar}-{baz}'


def test_asset_class_attribute_value_calculation_is_strict():
    class TestAsset(Asset):
        foo = '{bar}-{baz}'
        bar = 'bar'

    with pytest.raises(errors.ValueSubstitutionError):
        TestAsset.foo()
