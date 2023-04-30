from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import re
from typing import List, Tuple
from common import Directories, MapStructure
from snitch import Snitch
from file_io import write_content, get_sites_dict
from time import sleep
from logger import logger


def scrape(headless_operation: bool = False) -> Tuple[List[str], List[str]]:
    """
Returns (broken_sites, sites_with_manchester_ref)
    """
    logger.debug("Setting options")
    opts = Options()
    opts.headless = headless_operation
    logger.debug("Starting driver")
    driver = Firefox(options=opts)
    sites_with_manchester_ref = []
    working_sites = []
    dest_directory = Directories.ERRORS
    SITES = get_sites_dict()
    for name, map in SITES.items():
        page = map[MapStructure.PAGE]
        main_content = map[MapStructure.MAIN_CONTENT]
        snitch = Snitch(dest_directory=dest_directory, web_page_alias=name)

        logger.info(f"accessing website: {name}")
        text = ''
        with snitch.context_manager():
            driver.get(url=page)
            sleep(1)
            text = driver.find_element(by=By.XPATH, value=main_content).text
            write_content(text=text, source=name)
            logger.info("Scraping for the word 'Manchester'")
            found_manchester = contains_manchester(text=text)
            working_sites.append(name)
            if found_manchester:
                logger.info("Manchester found!")
                sites_with_manchester_ref.append(name)
    driver.quit()
    broken_sites = find_broken_sites(successfully_used_sites=working_sites)
    return (broken_sites, sites_with_manchester_ref)


def find_broken_sites(successfully_used_sites: List[str]) -> List[str]:
    SITES = get_sites_dict()
    all_sites = set(SITES.keys())
    working_sites = set(successfully_used_sites)
    broken_sites = all_sites.difference(working_sites)
    return list(broken_sites)


def contains_manchester(text: str) -> bool:
    manchester = r'.*[M|m][A|a][N|n][C|c][H|h][E|e][S|s][T|t][E|e][R|r].*'
    pattern = re.compile(manchester)
    match = re.search(pattern=pattern, string=text)
    return False if match is None else True
