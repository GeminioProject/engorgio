import queue

from engordio.scanner_worker import scanner_worker
from engordio.signals import Scan, Decompress


def test_call_scanner_with_file():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()

    called_with = None
    def scanner_scan(filepath):
        nonlocal called_with
        called_with = filepath
        if False:
            yield

    scanner_worker('FOO', scan_queue, decompress_queue, scanner_scan)

    assert called_with == 'FOO'


def test_add_to_scan_queue_scan_signals_from_scanner():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()

    def scanner_scan(filepath):
        yield Scan(filepath)

    scanner_worker('FOO', scan_queue, decompress_queue, scanner_scan)

    assert scan_queue.get_nowait() == 'FOO'


def test_add_to_decompress_queue_decompress_signals_from_scanner():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()

    def scanner_scan(filepath):
        yield Decompress(filepath)

    scanner_worker('FOO', scan_queue, decompress_queue, scanner_scan)

    assert decompress_queue.get_nowait() == 'FOO'
