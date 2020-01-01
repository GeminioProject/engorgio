"""
Scanner
=======

Find files to decompress.


"""
import os

from engorgio.entity import Entity
from engorgio.signals import DirFound
from engorgio.signals import FileFound
from engorgio.signals import SpecialFileFound
from engorgio.signals import SymlinkFound
from engorgio.signals import UserScanRequested


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


class Scanner(Entity):
    def _configure(self):
        pass

    def _prepare(self):
        self._attach(UserScanRequested, self.on_user_scan_requested)
        self._attach(DirFound, self.on_dir_found)

    def on_user_scan_requested(self, signal):
        classify_path(signal.path).emit()

    def on_dir_found(self, signal):
        for s in scandir(signal.path):
            s.emit()
