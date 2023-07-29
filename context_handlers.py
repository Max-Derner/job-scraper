from common import format_exception
from file_io import write_exception_report
from emailer import send_emergency_email
from logger import logger


class ExceptionSnitch:

    dest_directory: str
    web_page_alias: str

    def __init__(self, dest_directory: str, web_page_alias: str):
        self.dest_directory = dest_directory
        self.web_page_alias = web_page_alias

    class _WriteExceptionContextHandler:

        dest_directory: str
        web_page_alias: str

        def __init__(self, dest_directory: str, web_page_alias: str) -> None:
            self.dest_directory = dest_directory
            self.web_page_alias = web_page_alias

        def __enter__(self):
            logger.debug("Working safely to stop exceptions.")

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_val:
                write_exception_report(
                    dest_directory=self.dest_directory,
                    web_page_alias=self.web_page_alias,
                    exception_type=exc_type,
                    exception_traceback=exc_tb,
                    exception_value=exc_val
                )
                return True

    def context_manager(self):
        return self._WriteExceptionContextHandler(
            dest_directory=self.dest_directory,
            web_page_alias=self.web_page_alias
        )

    class _EmailExceptionContextHandler:

        def __enter__(self):
            logger.debug("Working safely to email exceptions.")

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_val:
                warning_message = ''
                warning_message += 'Shut down imminent! An unexpected exception has occurred!\n'  # noqa: E501
                warning_message += 'Attempting to send out emergency email!\n'
                warning_message += 'Logging exception before it\'s too late!'
                logger.warning(warning_message)
                formatted_exception = format_exception(
                    exception_type=exc_type,
                    exception_value=exc_val,
                    exception_traceback=exc_tb
                )
                logger.critical(formatted_exception)
                send_emergency_email(formatted_exception=formatted_exception)
                logger.info("Email successfully sent!")

            return False

    # This is the last line of defense against exceptions and is used to wrap main
    @classmethod
    def super_snitch_wrapper(cls, func):
        def wrapper(*args, **kwargs):
            with cls._EmailExceptionContextHandler():
                func(*args, **kwargs)
        return wrapper
