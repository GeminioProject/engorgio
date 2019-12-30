import queue

import pytest

from engordio.scanner_worker import dispatch_signals
from engordio.signals import DirFound, FileFound


def test_add_to_scan_queue_scan_signals_from_scanner():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()
    path = object()

    dispatch_signals(scan_queue, decompress_queue, [DirFound(path)])

    assert scan_queue.get_nowait() == path


def test_add_to_decompress_queue_decompress_signals_from_scanner():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()
    path = object()

    dispatch_signals(scan_queue, decompress_queue, [FileFound(path)])

    assert decompress_queue.get_nowait() == path


def test_raises_if_unknown_signal():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()
    path = object()

    with pytest.raises(ValueError):
        dispatch_signals(scan_queue, decompress_queue, [object()])
