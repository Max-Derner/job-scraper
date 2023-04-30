from emailer import (
    EmailCollection,
    send_emails,
    compose_help_email,
    compose_job_alert_email
)
from logger import logger
from web_scraper import scrape
from common import EmailAddressKeys
from snitch import Snitch
from futils import archive_artefacts
from file_io import get_email_address


@Snitch.super_snitch_wrapper
def main():
    logger.info("Starting emailer!")
    emails = EmailCollection()
    logger.info("Starting to scrape sites")
    broken_sites, sites_with_manchester_ref = scrape()
    sites_are_broken = len(broken_sites) > 0
    jobs_were_found = len(sites_with_manchester_ref) > 0
    should_send_emails = sites_are_broken or jobs_were_found
    if sites_are_broken:
        logger.info("Some sites were broken.")
        admin_addr = get_email_address(email_alias=EmailAddressKeys.ADMIN)
        emails.add_email(
            compose_help_email(broken_sites=broken_sites, dest_addr=admin_addr)
        )
    if jobs_were_found:
        logger.info("Some jobs were found.")
        target_addr = get_email_address(email_alias=EmailAddressKeys.TARGET)
        emails.add_email(
            compose_job_alert_email(
                sites_with_hit=sites_with_manchester_ref,
                dest_addr=target_addr
                )
        )
    if should_send_emails:
        logger.info("Sending the appropriate email(s).")
        send_emails(emails=emails)
    else:
        logger.info("No emails to send today.")
    archive_artefacts()


if __name__ == "__main__":
    main()
