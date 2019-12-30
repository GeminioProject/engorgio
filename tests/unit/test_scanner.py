import tempfile
import inspect

from engordio.signals import FileFound, DirFound
from engordio.scanner import scan


def test_return_a_decompress_if_file():
    with tempfile.NamedTemporaryFile() as file:
        assert list(scan(file.name)) == [FileFound(path=file.name)]


def test_scan_is_a_generator():
    assert inspect.isgeneratorfunction(scan)


def test_return_an_empty_list_if_dir_empty():
    with tempfile.TemporaryDirectory() as filepath:
        assert list(scan(filepath)) == []


def test_return_a_list_of_signals_if_dir():
    with tempfile.TemporaryDirectory() as path:
        with tempfile.NamedTemporaryFile(dir=path) as file, tempfile.TemporaryDirectory(dir=path) as subdir:
            assert set(scan(path)) == {FileFound(path=file.name), DirFound(path=subdir)}
