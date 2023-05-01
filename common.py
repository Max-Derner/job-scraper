from traceback import TracebackException
from types import TracebackType
from typing import Type
from enum import Enum
from datetime import datetime

ARTEFACTS_DIR = 'artefacts'
ARCHIVE_DIR = "archives"


def utc_now() -> datetime:
    return datetime.utcnow()


def format_exception(exception_type: Type[BaseException],
                     exception_value: BaseException,
                     exception_traceback: TracebackType) -> str:
    traceback_exception = TracebackException(exc_type=exception_type,
                                             exc_value=exception_value,
                                             exc_traceback=exception_traceback)
    formatted_trace_back = '\n'.join(traceback_exception.format(chain=True))
    return formatted_trace_back


class EmailAddressKeys(str, Enum):
    ADMIN = "ADMIN"
    TARGET = "TARGET"
    ROBOT = "ROBOT"


class Directories(str, Enum):
    ERRORS = f'{ARTEFACTS_DIR}/errors'
    DEBUG = f'{ARTEFACTS_DIR}/site_debug'


class MapStructure(str, Enum):
    PAGE = 'page'
    MAIN_CONTENT = 'main-content'
    LINES_TO_IGNORE = 'lines-to-ignore'
