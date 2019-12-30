from dataclasses import dataclass


@dataclass(frozen=True)
class DirFound:
    """A directory was found under the root path."""
    path: str


@dataclass(frozen=True)
class FileFound:
    """A file was found under the root path."""
    path: str


@dataclass
class UserScanRequested:
    """The user requested some path to be recusively decompressed."""
    #: The root path
    path: str


@dataclass
class Decompressed:
    """Some archive was succesfully decompressed."""
    #: Source archive path
    source: str
    #: Destination directory path
    path: str


@dataclass
class DecompressionDiscarded:
    """Some archive file was not decompressed by means of some policy."""
    #: Archive path
    path: str
    #: Why the archive wasn't decompressed
    reason: str


@dataclass
class DecompressionFailed:
    """The decompression of an archive failed."""
    #: Source archive path
    source: str
    #: Destination directory path
    path: str
    #: Some files were able to be decompressed
    partial: bool


@dataclass
class ContentAdded:
    """New (decompressed) content has been added under the root path."""
    #: Source archive path
    source: str
    #: Final destination path of the added content
    path: str

