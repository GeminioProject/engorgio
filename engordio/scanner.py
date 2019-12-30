from engordio.signals import FileFound


def scan(filepath):
    yield FileFound(path=filepath)
