from time import sleep

import pytest

from engorgio.entities.stopper import Stopper
from engorgio.signals import DirFound
from engorgio.signals import ExitRequested
from engorgio.signals import FileFound
from engorgio.signals import PathProcessingFinished
from engorgio.signals import SpecialFileFound
from engorgio.signals import SymlinkFound
from engorgio.signals import UserScanRequested


@pytest.mark.timeout(2)
def test_emit_exitrequested_if_all_files_were_processed():
    signals = set()

    def get_exit_requested(sender, signal):
        nonlocal signals
        signals.add(signal)

    ExitRequested.connect(get_exit_requested)

    stopper = Stopper(None)
    stopper.prepare()
    stopper.start()

    UserScanRequested(path=None).emit()
    DirFound(path=None).emit()
    FileFound(path=None).emit()
    SpecialFileFound(path=None).emit()
    SymlinkFound(path=None).emit()

    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()

    stopper.join()

    assert signals == {ExitRequested()}


@pytest.mark.timeout(3)
def test_dont_emit_exitrequested_if_there_are_pending_processing():
    signals = list()

    def get_exit_requested(sender, signal):
        nonlocal signals
        signals.append(signal)

    ExitRequested.connect(get_exit_requested)

    stopper = Stopper(None)
    stopper.prepare()
    stopper.start()

    UserScanRequested(path=None).emit()
    DirFound(path=None).emit()
    FileFound(path=None).emit()
    SpecialFileFound(path=None).emit()
    SymlinkFound(path=None).emit()

    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    PathProcessingFinished(path=None).emit()
    # We lack one PathProcessingFinished

    sleep(1)

    assert not signals

    ExitRequested().emit()
    stopper.join()
