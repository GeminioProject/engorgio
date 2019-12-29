import tempfile
import inspect

from engordio.signals import Decompress, Scan
from engordio.scanner import scan


def test_return_a_decompress_if_file():
    with tempfile.NamedTemporaryFile() as file:
        assert list(scan(file.name)) == [Decompress(path=file.name)]


def test_scan_is_a_generator():
    assert inspect.isgeneratorfunction(scan)


# def test_return_a_scan_if_dir():
#     with tempfile.TemporaryDirectory() as filepath:
#         assert list(scan(filepath)) == [Scan(path=filepath)]
