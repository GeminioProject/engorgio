from engordio.signals import Decompress


def scan(filepath):
    yield Decompress(path=filepath)
