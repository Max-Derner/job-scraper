from types import TracebackType
from typing import Type, Dict, Union
import json
from utilities.common import Directories, format_exception
from file_interactors.futils import ensure_directories_present


PASSWORD_FILE = "json_files/passwords.json"
EMAIL_ADDRESSES_FILE = "json_files/email_addresses.json"
WEBSITES_FILE = "json_files/sites.json"
APP_PASSWORD_KEY = "APP_PASSWORD"


def write_site_content(content: str, source: str):
    directory = Directories.DEBUG.value
    ensure_directories_present(directories=[directory])
    with open(f"{directory}/{source}.txt", mode='w') as io_wrapper:
        io_wrapper.write(content)


def write_exception_report(
        dest_directory: str,
        web_page_alias: str,
        exception_type: Type[BaseException],
        exception_value: BaseException,
        exception_traceback: TracebackType
        ):

    formatted_trace_back = format_exception(
        exception_type=exception_type,
        exception_value=exception_value,
        exception_traceback=exception_traceback
    )

    ensure_directories_present(directories=[dest_directory])
    exception_report_file_path = f"{dest_directory}/{web_page_alias}.txt"
    with open(exception_report_file_path, mode='w') as io_wrapper:
        report = ''
        report += '-~- EXCEPTION REPORT -~-'
        report += '\n'
        report += web_page_alias
        report += '\n'
        report += formatted_trace_back
        report += '\n\n\n'
        io_wrapper.write(report)


def get_email_address(email_alias: str) -> str:
    email_addr = _fetch_key_from_json_file(
        json_file=EMAIL_ADDRESSES_FILE,
        key=email_alias
        )
    if email_addr is None:
        raise KeyError(f"Key: '{email_alias}' returned no associated email address")  # noqa: E501
    else:
        return email_addr


def _fetch_key_from_json_file(json_file: str, key: str) -> Union[str, None]:
    with open(json_file, mode='r') as f:
        json_file_as_dict: Dict[str, str] = json.load(f)
    return json_file_as_dict.get(key)


def get_app_password() -> str:
    password = _fetch_key_from_json_file(
        json_file=PASSWORD_FILE,
        key=APP_PASSWORD_KEY
        )
    if password is None:
        raise KeyError(f"The key '{APP_PASSWORD_KEY}' is not valid for the password json file.")  # noqa: E501
    else:
        return password


def _fetch_whole_json_object(json_file: str) -> Dict:
    with open(json_file, mode='r') as f:
        json_file_as_dict = json.load(f)
    return json_file_as_dict


def get_sites_dict() -> Dict:
    return _fetch_whole_json_object(json_file=WEBSITES_FILE)
