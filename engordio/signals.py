"""
This module contains the signals used by `engordio` to exchange
information among its internal components.

Signals are immutable dataclasses containing some information produced
by one of the aforementioned components and received by any component(s)
interested on them.

To subscribe to a particular signal use the `connect` method passing a
handler.  For example to subscribe to the `UserScanRequested` signal do
the following::

>>> def handler(sender, signal):
...     print(f"{signal} received!")
...
>>> UserScanRequested.connect(handler)

Then at any time a `UserScanRequested` signal is emitted the `handler`
will be called::

>>> UserScanRequested(path="some path").emit()
UserScanRequested(path="some path") received!

"""
from dataclasses import dataclass

import blinker


class _Signal:
    """
    Base class for all signals.

    Provides utility functions to interface with `blinker`.

    """
    @property
    def _signal(self):
        """
        A singleton of a blinker signal named after the current class.

        """
        return blinker.signal(self.__class__.__name__)

    @classmethod
    def connect(cls, handler):
        """
        Connect the given handler with this signal type so it will
        receive any *emitted* signal of this type.

        The handler function should have the following signature:

        >>> def handler(sender, signal):
        ...     pass

        """
        blinker.signal(cls.__name__).connect(handler)

    def emit(self):
        """
        Emit this signal to all the handlers connected to this type of
        signal.

        """
        return self._signal.send(signal=self)


@dataclass(frozen=True)
class DirFound(_Signal):
    """A directory was found under the root path."""
    path: str


@dataclass(frozen=True)
class FileFound(_Signal):
    """A regular file was found under the root path."""
    path: str


@dataclass(frozen=True)
class SymlinkFound(_Signal):
    """A symlink to a regular file was found under the root path."""
    path: str


@dataclass(frozen=True)
class SpecialFileFound(_Signal):
    """A non regular file was found under the root path."""
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

