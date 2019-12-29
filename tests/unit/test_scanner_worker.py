import queue

from engordio.scanner_worker import scanner_worker


def test_call_scanner_with_file():
    scan_queue = queue.Queue()
    decompress_queue = queue.Queue()

    called_with = None
    def scanner_scan(filepath):
        nonlocal called_with
        called_with = filepath
        yield

    scan_queue.put('FOO')
    scanner_worker(scan_queue, decompress_queue, scanner_scan)

    assert called_with == 'FOO'

