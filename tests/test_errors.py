from pyventory.errors import PyventoryError


def test_pyventory_exception_format():
    test = 'test'
    example = 'example'
    e = PyventoryError(f'This is {test} format string {example}')
    assert str(e) == 'This is test format string example'


def test_pyventory_exception_format_degrade_on_non_string():
    e = PyventoryError(42, 'test')
    assert str(e) == "(42, 'test')"
