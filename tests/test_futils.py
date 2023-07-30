from file_interactors.futils import (
    ensure_directories_present,
    archive_artefacts,
    create_directory_if_not_exist
)
from utilities.common import ARTEFACTS_DIR, ARCHIVE_DIR
import os
import shutil
from unittest.mock import patch, Mock
from datetime import datetime


# indirectly tests create_directory_if_not_exist
def test_ensure_directories_present():
    # given
    cwd = os.getcwd()
    path1 = f"{cwd}/direct1/direct2/"
    path2 = "directory1/directory2"
    paths = [path1, path2]
    # when
    ensure_directories_present(directories=paths)
    # then
    assert os.path.exists(path=path1),\
         "Creating a directory structure specified from root did not work"
    shutil.rmtree(path="direct1")
    assert os.path.exists(path=path2),\
        "Creating a directory structure specified relatively did not work"
    shutil.rmtree(path="directory1")


@patch("file_interactors.futils.utc_now")
def test_archive_artefacts(utc_now: Mock):
    # given
    pretend_time = datetime(year=1970,
                            month=1,
                            day=2,
                            hour=12,
                            minute=34,
                            second=56,
                            microsecond=789012)
    iso_time = pretend_time.isoformat()
    utc_now.return_value = pretend_time
    if not os.path.exists(ARTEFACTS_DIR):
        os.mkdir(ARTEFACTS_DIR)
    test_file_file_path = f"{ARTEFACTS_DIR}/test_file"
    if not os.path.exists(test_file_file_path):
        os.mkdir(test_file_file_path)
    assert os.path.exists(test_file_file_path),\
        "An error has occurred in setting up the test"
    # when
    archive_artefacts()
    # then
    expected_file_path = f"{ARCHIVE_DIR}/{iso_time}"
    assert os.path.exists(expected_file_path),\
        "file was not correctly archived"
    shutil.rmtree(path=expected_file_path)


def tests_create_directory_if_not_exist_no_preexisting_file():
    # given
    directory = "test"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    assert not os.path.exists(directory), "test setup went wrong"
    # when
    create_directory_if_not_exist(directory=directory)
    # then
    correct_operation = os.path.exists(directory)
    if correct_operation:
        shutil.rmtree(directory)
    assert correct_operation,\
        "create_directory_if_not_exist did not successfully create directory"


def tests_create_directory_if_not_exist_yes_preexisting_file():
    # given
    directory = "test"
    if not os.path.exists(directory):
        os.mkdir(directory)
    assert os.path.exists(directory), "test setup went wrong"
    # when
    create_directory_if_not_exist(directory=directory)
    # then
    correct_operation = os.path.exists(directory)
    if correct_operation:
        shutil.rmtree(directory)
    assert correct_operation,\
        "create_directory_if_not_exist did not successfully create directory"

