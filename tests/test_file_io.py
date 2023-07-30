from unittest.mock import patch
from utilities.common import Directories
import pytest
import os
from file_interactors.file_io import (
    _fetch_key_from_json_file,
    get_app_password,
    get_email_address,
    write_site_content,
    get_sites_dict
)

MODULE = "file_interactors.file_io"

def test_fetch_key_from_json_file():
    # given
    expected_password = "cleverPassword123"
    returned_password = _fetch_key_from_json_file(json_file="json_files/i_am_a_test_file.json",
                                                  key="PASSWORD")
    assert expected_password == returned_password,\
        "incorrect password returned"


# indirectly tests get_arbitrary_password
@patch(f"{MODULE}.PASSWORD_FILE", "json_files/i_am_a_test_file.json")
def test_get_app_password_happy_path():
    # given
    expected_password = "iAmARobotsPasswordBleepBlorp!"
    # when
    returned_password = get_app_password()
    # then
    assert expected_password == returned_password,\
        "password not returned correctly"


# indirectly tests get_arbitrary_password
# given
@patch(f"{MODULE}.PASSWORD_FILE", "json_files/i_am_a_test_file.json")
@patch(f"{MODULE}.APP_PASSWORD_KEY", "something that doesn't exist")
def test_get_app_password_sad_path():
    with pytest.raises(KeyError):  # then
        # when
        _ = get_app_password()


# given
@patch(f"{MODULE}.PASSWORD_FILE", "non_existent_json_file_djshsiudhfnkdaj.json")
def test_get_app_password_extra_sad_path():
    with pytest.raises(FileNotFoundError):  # then
        # when
        _ = get_app_password()


# given
@patch(f"{MODULE}.EMAIL_ADDRESSES_FILE", "json_files/i_am_a_test_file.json")
def test_get_email_address_happy_path():
    expected_email = "mr.roboto@robot_place.org"
    # when
    returned_email = get_email_address(email_alias="ROBOT_EMAIL")
    # then
    assert expected_email == returned_email, "The email address was not returned correctly"


# given
@patch(f"{MODULE}.EMAIL_ADDRESSES_FILE", "json_files/i_am_a_test_file.json")
def test_get_email_address_sad_path():
    with pytest.raises(KeyError):  # then
        # when
        _ = get_email_address(email_alias="non-existent email alias")


# given
@patch(f"{MODULE}.EMAIL_ADDRESSES_FILE", "non_existent_json_file_djshsiudhfnkdaj.json")
def test_get_email_address_extra_sad_path():
    with pytest.raises(FileNotFoundError):  # then
        # when
        _ = get_email_address(email_alias="non-existent email alias")


def test_write_site_content():
    # given
    expected_directory = Directories.DEBUG.value
    expected_file = "my_test_file_987654"
    expected_file_path = f"{expected_directory}/{expected_file}.txt"
    expected_text = f"Hello, if you're reading this in a text file located at {expected_file_path}, then you should just delete the file.\n"
    expected_text += "It was an accident that this file got left behind, likely from a test failing and not removing the file."
    # when
    write_site_content(content=expected_text, source=expected_file)
    # then
    try:
        with open(file=expected_file_path, mode='r') as io_wrapper:
            actual_text = ''.join(io_wrapper.readlines())
        os.remove(expected_file_path)
    except Exception as e:
        assert False, f"expected file was not created in the correct location.\nSee error: {e.__repr__}"
    assert actual_text == expected_text, "Written text does not match what was expected"

# indirectly tests _fetch_whole_json_object
@patch(f"{MODULE}.WEBSITES_FILE", "json_files/i_am_a_test_file.json")
def test_get_sites_dict():
    # given
    expected_json = {'APP_PASSWORD': 'iAmARobotsPasswordBleepBlorp!',
                     'PASSWORD': 'cleverPassword123',
                     'ROBOT_EMAIL': 'mr.roboto@robot_place.org',
                     'WARNING': 'DO NOT CHANGE THIS FILE! TESTS RELY ON IT!'}
    # when
    actual_json = get_sites_dict()
    # then
    assert expected_json == actual_json
