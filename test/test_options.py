from ordutils.options import \
    validate_file_option, validate_dir_option, \
    validate_dict_option, validate_int_option, \
    validate_list_option, check_boolean_value
from tempfile import mkdtemp, NamedTemporaryFile
from schema import SchemaError

import pytest
import os


def test_validate_file_option_does_not_raise_exception_for_existing_file_if_file_should_exist():
    file = NamedTemporaryFile()
    file_name = file.name
    validate_file_option(file_name, "dummy")


def test_validate_file_option_does_not_raise_exception_for_non_existing_file_if_file_should_not_exist():
    file = NamedTemporaryFile()
    file_name = file.name
    file.close()
    validate_file_option(file_name, "dummy", should_exist=False)


def test_validate_file_option_raises_exception_for_non_existing_file_if_file_should_exist():
    file = NamedTemporaryFile()
    file_name = file.name
    file.close()
    with pytest.raises(SchemaError):
        validate_file_option(file_name, "dummy")


def test_validate_file_option_raises_exception_for_existing_file_if_file_should_not_exist():
    file = NamedTemporaryFile()
    file_name = file.name
    with pytest.raises(SchemaError):
        validate_file_option(file_name, "dummy", should_exist=False)


def test_validate_file_option_raises_exception_for_none_if_nullable_not_specified():
    with pytest.raises(SchemaError):
        validate_file_option(None, "dummy")


def test_validate_file_option_does_not_raise_exception_for_none_if_nullable_specified():
    validate_file_option(None, "dummy", nullable=True)


def test_validate_file_option_exception_message_contains_correct_info():
    file = NamedTemporaryFile()
    file_name = file.name
    file.close()

    msg = "dummy"
    with pytest.raises(SchemaError) as exc_info:
        validate_file_option(file_name, msg)

    check_exception_message(exc_info, msg, file_name)


def test_validate_dir_option_does_not_raise_exception_for_existing_dir_if_dir_should_exist():
    dir_path = mkdtemp()
    validate_dir_option(dir_path, "dummy")
    os.rmdir(dir_path)


def test_validate_dir_option_does_not_raise_exception_for_non_existing_dir_if_dir_should_not_exist():
    dir_path = mkdtemp()
    os.rmdir(dir_path)
    validate_dir_option(dir_path, "dummy", should_exist=False)


def test_validate_dir_option_raises_exception_for_non_existing_dir_if_dir_should_exist():
    dir_path = mkdtemp()
    os.rmdir(dir_path)
    with pytest.raises(SchemaError):
        validate_dir_option(dir_path, "dummy")


def test_validate_dir_option_raises_exception_for_existing_dir_if_dir_should_not_exist():
    dir_path = mkdtemp()
    with pytest.raises(SchemaError):
        validate_dir_option(dir_path, "dummy", should_exist=False)
    os.rmdir(dir_path)


def test_validate_dir_option_raises_exception_for_none_if_nullable_not_specified():
    with pytest.raises(SchemaError):
        validate_dir_option(None, "dummy")


def test_validate_dir_option_does_not_raise_exception_for_none_if_nullable_specified():
    validate_dir_option(None, "dummy", nullable=True)


def test_validate_dir_option_exception_message_contains_correct_info():
    dir_path = mkdtemp()
    os.rmdir(dir_path)

    msg = "dummy"
    with pytest.raises(SchemaError) as exc_info:
        validate_dir_option(dir_path, msg)

    check_exception_message(exc_info, msg, dir_path)


def test_validate_dict_option_returns_correct_dict_value():
    values_dict = {1: "one", 2: "two"}
    assert validate_dict_option(2, values_dict, "dummy") == "two"


def test_validate_dict_option_raises_exception_for_non_existent_key():
    values_dict = {1: "one", 2: "two"}
    with pytest.raises(SchemaError):
        validate_dict_option(3, values_dict, "dummy")


def test_validate_dict_option_exception_message_contains_correct_info():
    values_dict = {1: "one", 2: "two"}

    msg = "dummy"
    key = 3
    with pytest.raises(SchemaError) as exc_info:
        validate_dict_option(key, values_dict, msg)

    check_exception_message(exc_info, msg, key)


def test_validate_int_option_returns_correct_value():
    int_val = 1
    assert validate_int_option(str(1), "dummy") == int_val


def test_validate_int_option_raises_exception_for_non_int():
    with pytest.raises(SchemaError):
        validate_int_option("a", "dummy")


def test_validate_int_option_raises_exception_for_negative_if_nonneg_specified():
    with pytest.raises(SchemaError):
        validate_int_option(-1, "dummy", nonneg=True)


def test_validate_int_option_does_not_raise_exception_for_negative_if_nonneg_not_specified():
    validate_int_option(-1, "dummy")


def test_validate_int_option_raises_exception_for_none_if_nullable_not_specified():
    with pytest.raises(SchemaError):
        validate_int_option(None, "dummy")


def test_validate_int_option_does_not_raise_exception_for_none_if_nullable_specified():
    validate_int_option(None, "dummy", nullable=True)


def test_validate_int_option_exception_message_contains_correct_info():
    msg = "dummy"
    str_val = "abcde"
    with pytest.raises(SchemaError) as exc_info:
        validate_int_option(str_val, msg)

    check_exception_message(exc_info, msg, str_val)


def test_validate_list_option_returns_correct_number_of_items():
    num_items = 5
    separator = ";"
    option_string = (("dummy" + separator) * num_items)[:-1]
    assert len(validate_list_option(
        option_string, lambda x: x, separator)) == num_items


def test_validate_list_option_returns_transformed_objects():
    option_values = [1, 5, 10]
    separator = ","
    option_string = separator.join([str(v) for v in option_values])
    assert validate_list_option(option_string, int, separator) \
        == option_values


def test_validate_list_option_raises_exception_for_invalid_value():
    option_values = [1, 5, "ten"]
    separator = ","
    option_string = separator.join([str(v) for v in option_values])
    with pytest.raises(SchemaError):
        validate_list_option(option_string, int, separator)


def test_check_boolean_value_accepts_valid_true_strings():
    for option_string in ["true", "t", "yes", "y"]:
        assert check_boolean_value(option_string)
        assert check_boolean_value(option_string.upper())


def test_check_boolean_value_accepts_valid_false_strings():
    for option_string in ["false", "f", "no", "n"]:
        assert not check_boolean_value(option_string)
        assert not check_boolean_value(option_string.upper())


def test_check_boolean_value_raises_exception_for_invalid_string():
    with pytest.raises(Exception):
        check_boolean_value("not a boolean")


def check_exception_message(exc_info, *args):
    exc_msg = exc_info.value.message
    for arg in args:
        assert str(arg) in exc_msg
