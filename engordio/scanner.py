"""
Scanner
=======

Find files to decompress.


"""
import os

from engordio.signals import FileFound, DirFound, SymlinkFound, \
    SpecialFileFound


def classify_path(path):
    """
    Generate a signal based on the nature of the given path.

    """
    if os.path.islink(path):
        return SymlinkFound(path=path)
    elif os.path.isfile(path):
        return FileFound(path=path)
    elif os.path.isdir(path):
        return DirFound(path=path)
    else:
        return SpecialFileFound(path=path)


def scandir(path):
    """
    Generate a signal for every file and directory found in path.

    """
    with os.scandir(path) as dircontent:
        for entry in dircontent:
            if entry.is_symlink():
                yield SymlinkFound(path=entry.path)
            elif entry.is_file():
                yield FileFound(path=entry.path)
            elif entry.is_dir():
                yield DirFound(path=entry.path)
            else:
                yield SpecialFileFound(path=entry.path)
