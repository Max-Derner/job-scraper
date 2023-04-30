from futils import ensure_directories_present
import os
import shutil


def test_ensure_directories_present():
    cwd = os.getcwd()
    path1 = f"{cwd}/direct1/direct2/"
    path2 = "directory1/directory2"
    paths = [path1, path2]
    ensure_directories_present(directories=paths)
    assert os.path.exists(path=path1), "Creating a directory structure specified from root did not work"
    assert os.path.exists(path=path2), "Creating a directory structure specified relatively did not work"
    shutil.rmtree(path="direct1")
    shutil.rmtree(path="directory1")


