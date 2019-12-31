import inspect
import os
import tempfile


from engorgio.scanner import classify_path, scandir
from engorgio.signals import FileFound, DirFound, SymlinkFound, SpecialFileFound


def test_classify_path_returns_a_filefound_if_regular_file():
    with tempfile.NamedTemporaryFile() as file:
        assert classify_path(file.name) == FileFound(path=file.name)


def test_classify_path_returns_a_symlinkfound_if_symlink_to_regular_file():
    with tempfile.TemporaryDirectory() as path:
        filepath = os.path.join(path, 'regular_file')
        symlink_path = filepath + '_symlink'

        open(filepath, 'w').close()  # Equivalent to touch command
        os.symlink(filepath, symlink_path)

        assert classify_path(symlink_path) == SymlinkFound(path=symlink_path)


def test_classify_path_returns_a_specialfilefound_if_non_regular_file():
    with tempfile.TemporaryDirectory() as path:
        pipe_path = os.path.join(path, 'pipe')
        os.mkfifo(pipe_path)

        assert classify_path(pipe_path) == SpecialFileFound(path=pipe_path)


def test_classify_path_returns_a_dirfound_if_dir():
    with tempfile.TemporaryDirectory() as path:
        assert classify_path(path) == DirFound(path=path)


# TODO: test for other non regular files


def test_scandir_is_a_generator():
    assert inspect.isgeneratorfunction(scandir)


def test_scandir_returns_an_empty_list_if_dir_empty():
    with tempfile.TemporaryDirectory() as path:
        assert list(scandir(path)) == []


def test_scandir_return_a_symlinkfound_if_dir_contains_symlink_to_regular_file():
    with tempfile.TemporaryDirectory() as path:
        filepath = os.path.join(path, 'regular_file')
        symlink_path = filepath + '_symlink'

        open(filepath, 'w').close()  # Equivalent to touch command
        os.symlink(filepath, symlink_path)

        assert SymlinkFound(path=symlink_path) in set(scandir(path))


def test_scandir_return_a_specialfilefound_if_dir_contains_a_non_regular_file():
    with tempfile.TemporaryDirectory() as path:
        pipe_path = os.path.join(path, 'pipe')
        os.mkfifo(pipe_path)

        assert list(scandir(path)) == [SpecialFileFound(path=pipe_path)]


def test_scandir_return_a_filefound_if_dir_contains_a_regular_file():
    with tempfile.TemporaryDirectory() as path:
        filepath = os.path.join(path, 'regular_file')
        open(filepath, 'w').close()  # Equivalent to touch command

        assert list(scandir(path)) == [FileFound(path=filepath)]


def test_scandir_returns_a_dirfound_if_dir_contains_dir():
    with tempfile.TemporaryDirectory() as path1:
        with tempfile.TemporaryDirectory(dir=path1) as path2:
            assert list(scandir(path1)) == [DirFound(path=path2)]


def test_scandir_return_a_list_of_signals_if_dir_contains_dotfile():
    with tempfile.TemporaryDirectory() as path:
        with tempfile.NamedTemporaryFile(prefix='.', dir=path) \
                as file, tempfile.TemporaryDirectory(dir=path) as subdir:
            assert set(scandir(path)) == {FileFound(path=file.name), DirFound(path=subdir)}
