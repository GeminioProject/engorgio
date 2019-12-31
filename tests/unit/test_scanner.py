import inspect
import os
import tempfile


from engordio.scanner import scan
from engordio.signals import FileFound, DirFound, SymlinkFound, SpecialFileFound


def test_return_a_filefound_if_regular_file():
    with tempfile.NamedTemporaryFile() as file:
        assert list(scan(file.name)) == [FileFound(path=file.name)]


def test_return_a_symlinkfound_if_symlink_to_regular_file():
    with tempfile.TemporaryDirectory() as path:
        filepath = os.path.join(path, 'regular_file')
        symlink_path = filepath + '_symlink'

        open(filepath, 'w').close()  # Equivalent to touch command
        os.symlink(filepath, symlink_path)

        assert list(scan(symlink_path)) == [SymlinkFound(path=symlink_path)]


def test_return_a_specialfilefound_if_non_regular_file():
    with tempfile.TemporaryDirectory() as path:
        pipe_path = os.path.join(path, 'pipe')
        os.mkfifo(pipe_path)

        assert list(scan(pipe_path)) == [SpecialFileFound(path=pipe_path)]


# TODO: test for other non regular files


def test_scan_is_a_generator():
    assert inspect.isgeneratorfunction(scan)


def test_return_an_empty_list_if_dir_empty():
    with tempfile.TemporaryDirectory() as path:
        assert list(scan(path)) == []


def test_return_a_list_of_signals_if_dir():
    with tempfile.TemporaryDirectory() as path:
        with tempfile.NamedTemporaryFile(dir=path) as file, tempfile.TemporaryDirectory(dir=path) as subdir:
            assert set(scan(path)) == {FileFound(path=file.name), DirFound(path=subdir)}


def test_return_a_symlinkfound_if_dir_contains_symlink_to_regular_file():
    with tempfile.TemporaryDirectory() as path:
        filepath = os.path.join(path, 'regular_file')
        symlink_path = filepath + '_symlink'

        open(filepath, 'w').close()  # Equivalent to touch command
        os.symlink(filepath, symlink_path)

        assert set(scan(path)) == {FileFound(path=filepath), SymlinkFound(path=symlink_path)}


def test_return_a_specialfilefound_if_dir_contains_a_non_regular_file():
    with tempfile.TemporaryDirectory() as path:
        pipe_path = os.path.join(path, 'pipe')
        os.mkfifo(pipe_path)

        assert list(scan(path)) == [SpecialFileFound(path=pipe_path)]


def test_return_a_list_of_signals_if_dir_contains_dotfile():
    with tempfile.TemporaryDirectory() as path:
        with tempfile.NamedTemporaryFile(prefix='.', dir=path) as file, tempfile.TemporaryDirectory(dir=path) as subdir:
            assert set(scan(path)) == {FileFound(path=file.name), DirFound(path=subdir)}
