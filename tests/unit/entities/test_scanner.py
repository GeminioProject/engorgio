from unittest.mock import patch
import inspect
import os
import tempfile


from engorgio.entities.scanner import classify_path, scandir, Scanner
from engorgio.signals import DirFound
from engorgio.signals import ExitRequested
from engorgio.signals import FileFound
from engorgio.signals import SpecialFileFound
from engorgio.signals import SymlinkFound
from engorgio.signals import UserScanRequested


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


def test_scanner_find_regular_file_with_classify_path_on_userscanrequested():
    found = set()

    def get_found_files(sender, signal):
        nonlocal found
        found.add(signal)

    FileFound.connect(get_found_files)
    DirFound.connect(get_found_files)
    SpecialFileFound.connect(get_found_files)
    SymlinkFound.connect(get_found_files)

    with patch('engorgio.entities.scanner.classify_path') as classify_path:
        with tempfile.TemporaryDirectory() as path:
            filename = os.path.join(path, 'foo.txt')
            open(filename, 'w').close()  # Touch foo.txt

            classify_path.return_value = FileFound(path=filename)

            config = {}
            scanner = Scanner(config)
            scanner.prepare()
            scanner.start()
            UserScanRequested(path=filename).emit()
            ExitRequested().emit()
            scanner.join()

            classify_path.assert_called_once_with(filename)
            assert found == set({FileFound(path=filename)})


def test_scanner_find_directory_contents_on_dirfound():
    found = set()

    def get_found_files(sender, signal):
        nonlocal found
        found.add(signal)

    FileFound.connect(get_found_files)
    SymlinkFound.connect(get_found_files)

    with tempfile.TemporaryDirectory() as path:
        filename = os.path.join(path, 'foo.txt')
        open(filename, 'w').close()  # Touch foo.txt

        linkname = os.path.join(path, 'foo.lnk')
        os.symlink(filename, linkname)

        config = {}
        scanner = Scanner(config)
        scanner.prepare()
        scanner.start()
        DirFound(path=path).emit()
        ExitRequested().emit()
        scanner.join()

        assert found == set({FileFound(path=filename),
                             SymlinkFound(path=linkname)})
