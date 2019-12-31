import os

from engordio.signals import FileFound, DirFound, SymlinkFound, SpecialFileFound


def scan(path):
    """
    Generate a signal for every file and directory found in path.

    On files it generates a `FileFound` signal and `DirFound` on directories.

    """
    if os.path.isfile(path):
        if os.path.islink(path):
            yield SymlinkFound(path=path)
        else:
            yield FileFound(path=path)
    elif os.path.isdir(path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    if entry.is_symlink():
                        yield SymlinkFound(path=entry.path)
                    else:
                        yield FileFound(path=entry.path)
                elif entry.is_dir():
                    yield DirFound(path=entry.path)
                else:
                    yield SpecialFileFound(path=entry.path)
    else:
        yield SpecialFileFound(path=path)
