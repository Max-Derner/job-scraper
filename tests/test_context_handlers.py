from context_handlers import ExceptionSnitch
from unittest.mock import patch, Mock
import pytest


class TestException(Exception):
    pass


def throw_error():
    raise TestException("I am a test exception! Look at me go!")

TEST_DIR = "test"
ALIAS = "some_web_page"


@patch("context_handlers.send_emergency_email")
def tests_wrapper_feature(send_emergency_email: Mock):
    # given
    snitch = ExceptionSnitch(dest_directory=TEST_DIR, web_page_alias=ALIAS)
    @snitch.super_snitch_wrapper
    def wrapped_throw_error():
        throw_error()
    # when
    with pytest.raises(TestException):
        wrapped_throw_error()
    # then
    send_emergency_email.assert_called_once()


@patch("context_handlers.write_exception_report")
def tests_write_exception_context_manager(write_exception_report: Mock):
    # given
    snitch = ExceptionSnitch(dest_directory=TEST_DIR, web_page_alias=ALIAS)
    # when
    with snitch.context_manager():
        throw_error()
    # then
    write_exception_report.assert_called_once()





