import os

from engordio.signals import FileFound, DirFound


def scan(path):
    if os.path.isfile(path):
        yield FileFound(path=path)
    if os.path.isdir(path):
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    if entry.is_file():
                        yield FileFound(path=entry.path)
                    else:
                        yield DirFound(path=entry.path)
