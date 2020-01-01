import libarchive
import os
import tempfile

from engorgio.signals import Decompressed, DecompressionFailed


def decompress(filepath, sandbox):
    """
    Decompress filepath on a temporary directory in sandbox.

    """
    new_filepath = tempfile.mkdtemp(dir=sandbox)

    previous_workdir = os.getcwd()
    os.chdir(new_filepath)

    try:
        libarchive.extract_file(filepath)
        os.chdir(previous_workdir)
        return Decompressed(source=filepath, path=new_filepath)
    except libarchive.exception.ArchiveError as e:
        os.chdir(previous_workdir)
        # If there are more than 2 files on new_filepath, implies there is a partial decompression
        partial_decompression = len(os.listdir(new_filepath)) > 2
        return DecompressionFailed(source=filepath, path=new_filepath, partial=partial_decompression, error=e)
