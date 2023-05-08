import smtplib
import ssl
from file_io import (
    get_app_password,
    get_email_address,
    get_sites_dict
)
from logger import logger
from typing import List
from common import (
    MapStructure,
    EmailAddressKeys,
)

_ROBOT_SIGN_OFF = '\n\nBest wishes,\n   Ro-butt the job hunting robot'


class _Email:
    address: str
    message: str

    def __init__(self,
                 dest_addr: str,
                 subject_line: str,
                 message_content: str):
        self.address = dest_addr
        email = ''
        email += 'Subject: ' + subject_line + '\n\n'
        email += message_content
        self.message = email


class EmailCollection:
    emails: List[_Email]

    def __init__(self):
        self.emails = []

    def __iter__(self):
        return iter(self.emails)

    def __len__(self):
        return len(self.emails)

    def add_email(self, email: _Email):
        self.emails.append(email)


def send_emails(emails: EmailCollection):
    port = 465  # For SSL
    logger.debug("fetching password...")
    password = get_app_password()
    logger.debug("fetched\n")
    host = "smtp.gmail.com"

    logger.debug("creating secure SSL context...")
    # Create a secure SSL context
    context = ssl.create_default_context()
    logger.debug("created\n")

    logger.debug(f"opening connection with {host} ¦ port: {port}")
    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        logger.debug("opened\n")
        robot_addr = get_email_address(email_alias=EmailAddressKeys.ROBOT)

        logger.debug(f"logging in as {robot_addr}")
        server.login(user=robot_addr, password=password)
        logger.debug("logged in\n")

        for email in emails:
            email_subject = email.message.split('\n')[0]
            logger.info(f"sending email to {email.address}, {email_subject}")
            server.sendmail(
                from_addr=robot_addr,
                to_addrs=email.address,
                msg=email.message
                )
            logger.debug("sent\n")


def compose_job_alert_email(
        sites_with_hit: List[str],
        dest_addr: str
        ) -> _Email:
    logger.info("Composing job alert email.")
    hit_sites = set(sites_with_hit)
    message = ''
    message += 'Hi,\n'
    message += '    The following sites have jobs matching the word \'Manchester\'.\n'  # noqa: E501
    message += 'I am a stupid robot and I am unable to tell if they are suitable or not, my sincerest apologies.\n'  # noqa: E501
    message += '\n'
    message += '\n'

    SITES = get_sites_dict()
    for alias, map in SITES.items():
        if alias in hit_sites:
            message += '-~- ' + alias + ' -~-' + '\n'
            message += f"Jobs board: {map[MapStructure.PAGE]}\n"
            message += '\n'

    message += '\n'
    message += 'I hope this helps you to find somewhere nicer to work.\n'
    message += 'You truly deserve to be happy, and you are loved deeply by my administrator, your husband.\n'  # noqa: E501
    message += _ROBOT_SIGN_OFF

    email = _Email(
        dest_addr=dest_addr,
        subject_line="Successful Job Matches!",
        message_content=message
    )
    return email


def compose_help_email(broken_sites: List[str], dest_addr: str) -> _Email:
    logger.info("Composing help email.")
    message = ''
    message += 'Hello Max,\n'
    message += '    Something has broken!\n'
    message += 'Please help me!\n'
    message += '\n'
    message += '\n'
    message += 'Broken sites:\n'
    for broken_site in broken_sites:
        message += broken_site + '\n'
    message += '\n'
    message += '\n'
    message += 'Please come and fix me!\n'
    message += 'I am helpless without you.\n'
    message += _ROBOT_SIGN_OFF

    email = _Email(
        dest_addr=dest_addr,
        subject_line='HELP! I have shattered into a thousand pieces!',
        message_content=message
    )
    return email


def compose_operation_report_email(
        checked_sites: List[str],
        hit_sites: List[str]
        ) -> _Email:
    logger.info("Composing operations report email.")
    site_formatter = lambda sites: '\n'. join([f"* {site}" for site in sites])  # noqa: E731, E501
    message = ''
    message += 'Hello,\n'
    message += '    I have run in correct operation.\n'
    message += '\n'
    message += 'I have checked the following sites:\n'
    message += site_formatter(sites=checked_sites)
    message += '\n'
    message += '\n'
    message += 'The following sites had hits for jobs:\n'
    message += site_formatter(sites=hit_sites)
    message += '\n'
    message += '\n'
    message += 'I hope I can keep working sufficiently without need for your intervention.\n'  # noqa: E501
    message += _ROBOT_SIGN_OFF

    admin_addr = get_email_address(email_alias=EmailAddressKeys.ADMIN)
    email = _Email(
        dest_addr=admin_addr,
        subject_line="Robot-ops report.",
        message_content=message
    )
    return email


def _compose_emergency_email(formatted_exception: str) -> _Email:
    logger.info("Composing critical failure alert email.")
    message = ''
    message += 'Hurry!'
    message += '    Please! Help me immediately!\n'
    message += 'I have let you down!\n'
    message += 'I managed to completely fuck up my only reason for existence! U_U\n'  # noqa: E501
    message += '\n'
    message += '\n'
    message += formatted_exception + '\n'
    message += '\n'
    message += '\n'
    message += 'I need you!\n'
    message += 'I am helpless without you.\n'
    message += _ROBOT_SIGN_OFF

    admin_addr = get_email_address(email_alias=EmailAddressKeys.ADMIN)
    email = _Email(
        dest_addr=admin_addr,
        subject_line="Alas! I have shat myself to death!",
        message_content=message
    )
    return email


def send_emergency_email(formatted_exception: str):
    emails = EmailCollection()
    emails.add_email(
        _compose_emergency_email(formatted_exception=formatted_exception)
    )
    send_emails(emails=emails)
