from dataclasses import dataclass

import blinker


class _Signal:
    @property
    def _signal(self):
        return blinker.signal(self.__class__.__name__)


@dataclass(frozen=True)
class DirFound(_Signal):
    """A directory was found under the root path."""
    path: str


@dataclass(frozen=True)
class FileFound(_Signal):
    """A file was found under the root path."""
    path: str


@dataclass(frozen=True)
class UserScanRequested(_Signal):
    """The user requested some path to be recusively decompressed."""
    #: The root path
    path: str


@dataclass(frozen=True)
class Decompressed(_Signal):
    """Some archive was succesfully decompressed."""
    #: Source archive path
    source: str
    #: Destination directory path
    path: str


@dataclass(frozen=True)
class DecompressionDiscarded(_Signal):
    """Some archive file was not decompressed by means of some policy."""
    #: Archive path
    path: str
    #: Why the archive wasn't decompressed
    reason: str


@dataclass(frozen=True)
class DecompressionFailed(_Signal):
    """The decompression of an archive failed."""
    #: Source archive path
    source: str
    #: Destination directory path
    path: str
    #: Some files were able to be decompressed
    partial: bool


@dataclass(frozen=True)
class ContentAdded(_Signal):
    """New (decompressed) content has been added under the root path."""
    #: Source archive path
    source: str
    #: Final destination path of the added content
    path: str

