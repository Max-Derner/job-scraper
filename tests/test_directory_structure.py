from utilities.common import Directories


def tests_directories():
    assert Directories.ERRORS.value == "artefacts/errors",\
        "something is broken with your Directories enum"
    assert Directories.DEBUG.value == "artefacts/site_debug",\
        "something is broken with your Directories enum"
