import argparse
from internet_interactors.emailer import (
    EmailCollection,
    send_emails,
    compose_help_email,
    compose_job_alert_email,
    compose_operation_report_email
)
from utilities.logger import logger
from internet_interactors.web_scraper import scrape
from utilities.common import EmailAddressKeys
from utilities.context_handlers import ExceptionSnitch
from file_interactors.futils import archive_artefacts
from file_interactors.file_io import get_email_address


@ExceptionSnitch.super_snitch_wrapper
def main():
    logger.info("Parsing CMD arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless-operation', action='store_true')
    args = parser.parse_args()
    headless_operation = args.headless_operation
    logger.info(f"Headless operation is set to: {headless_operation}")

    logger.info("\nStarting up!")
    emails = EmailCollection()
    logger.info("Starting to scrape sites")
    broken_sites, working_sites, sites_with_manchester_ref = scrape(
        headless_operation=headless_operation
        )
    sites_are_broken = len(broken_sites) > 0
    jobs_were_found = len(sites_with_manchester_ref) > 0
    logger.info("\nComposing relevant emails.")
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
    emails.add_email(
        compose_operation_report_email(
            checked_sites=working_sites,
            hit_sites=sites_with_manchester_ref
        )
    )
    if len(emails) > 0:
        logger.info("\nSending the appropriate email(s).")
        send_emails(emails=emails)

    archive_artefacts()


if __name__ == "__main__":
    main()
