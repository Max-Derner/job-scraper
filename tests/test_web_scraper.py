from web_scraper import(
    contains_manchester,
    find_broken_sites,
    remove_ignored_lines,
    scrape
    )
import pytest
from unittest.mock import patch

#### contains_manchester
#### find_broken_sites
#### remove_ignored_lines
# scrape <- not tested

# given
@pytest.mark.parametrize('manchester_present, text', [
    (True, 'Manchester'),
    (True, 'MANCHESTER'),
    (True, 'manchester'),
    (True, 'mANCHESTER'),
    (True, 'somenonsensetestmanchestersomemorenonsense'),
    (True, 'MaNcHeStEr'),
    (False, 'some other place'),
    (False, 'Menchester'),
    (False, 'bleep bloop blorp')
])
def tests_contains_manchester(manchester_present: bool, text: str):
    # when
    result = contains_manchester(text=text)
    # then
    assert result == manchester_present,\
        f"Incorrect result, 'Manchester' was\
              {'' if manchester_present else 'not'} present"

# given
@patch("file_io.WEBSITES_FILE", "i_am_a_test_file.json")
def tests_find_broken_sites():
    successfully_used_sites = ["PASSWORD",
                               "APP_PASSWORD",
                               "THIS IS NOT IN THE JSON"]
    expected_broken_sites = set(["ROBOT_EMAIL",
                                 "WARNING"])
    # when
    broken_sites = find_broken_sites(
        successfully_used_sites=successfully_used_sites
        )
    # then 
    assert expected_broken_sites == broken_sites,\
        "Broken sites incorrectly parsed"

def tests_remove_ignored_lines():
    # given
    text = "I am a multi line bit of text.\nI have many lines.\nIt is fun to have lines.\nI don't have too many lines though.\nI am restrained and easy on the eyes like that."

    lines_to_remove = [1,3,5]

    expected_text = "\nI have many lines.\n\nI don't have too many lines though.\n"
    # when
    returned_text = remove_ignored_lines(
        unedited_text=text,
        lines_to_ignore=lines_to_remove
        )
    # then
    assert returned_text == expected_text,\
    "The lines were not removed correctly"

