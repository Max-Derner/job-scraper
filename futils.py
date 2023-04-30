import shutil
import os
from typing import List
from common import utc_now, ARCHIVE_DIR, ARTEFACTS_DIR


def create_directory_if_not_exist(directory: str):
    if not os.path.exists(directory):
        os.mkdir(directory)


def ensure_directories_present(directories: List[str]):
    directories_to_ensure = []
    for directory in directories:
        from_root = False
        if directory[0] == '/':
            from_root = True
            directory = directory[1:]
        directory_structure = directory.split('/')
        for idx in range(1, len(directory_structure)+1):
            directory = '/'.join(directory_structure[:idx])
            if from_root:
                directory = '/' + directory
            directories_to_ensure.append(directory)
    for directory in directories_to_ensure:
        create_directory_if_not_exist(directory=directory)


def archive_artefacts():
    utcnow = str(utc_now().isoformat())
    archive_dest = f"{ARCHIVE_DIR}/{utcnow}"
    shutil.move(src=ARTEFACTS_DIR, dst=archive_dest)
