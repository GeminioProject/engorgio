import os
import tempfile

from engorgio.decompressor import decompress
from engorgio.signals import Decompressed, DecompressionFailed


def test_returns_decompressed_on_success(data_path):
    with tempfile.TemporaryDirectory() as sandbox:
        regular_file_path = os.path.join(data_path, 'regularfile.zip')
        assert isinstance(decompress(regular_file_path, sandbox), Decompressed)


def test_check_if_decompress_was_successful_with_a_regular_zip(data_path):
    with tempfile.TemporaryDirectory() as sandbox:
        regular_file_path = os.path.join(data_path, 'regularfile.zip')

        regular_file_decompressed = decompress(regular_file_path, sandbox)

        with open(os.path.join(regular_file_decompressed.path, 'info.txt'), 'r') as f:
            read_data = f.read()

        assert read_data == 'Words are, in my not-so-humble opinion, our most inexhaustible source of magic.\n'


def test_returns_decompressedfailed_with_a_malformed_compressed_file(data_path):
    with tempfile.TemporaryDirectory() as sandbox:
        regular_file_path = os.path.join(data_path, 'malformed.zip')
        assert isinstance(decompress(regular_file_path, sandbox), DecompressionFailed)
