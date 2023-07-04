from unittest.mock import Mock, patch
import pytest
from file_io import (
    _fetch_key_from_json_file,
    PASSWORD_FILE,
    get_app_password
)


def test_fetch_key_from_json_file():
    # given
    expected_password = "cleverPassword123"
    returned_password = _fetch_key_from_json_file(json_file="i_am_a_test_file.json",
                                                  key="PASSWORD")
    assert expected_password == returned_password,\
        "incorrect password returned"


# indirectly tests get_arbitrary_password
@patch("file_io.PASSWORD_FILE", "i_am_a_test_file.json")
def test_get_app_password_happy_path():
    # given
    expected_password = "iAmARobotsPasswordBleepBlorp!"
    # when
    returned_password = get_app_password()
    # then
    assert expected_password == returned_password,\
        "password not returned correctly"


# indirectly tests get_arbitrary_password
@patch("file_io.PASSWORD_FILE", "i_am_a_test_file.json")
@patch("file_io.APP_PASSWORD_KEY", "something that doesn't exist")
def test_get_app_password_sad_path():
    # given
    expected_password = "iAmARobotsPasswordBleepBlorp!"
    with pytest.raises(KeyError):  # then
        # when
        _ = get_app_password()
