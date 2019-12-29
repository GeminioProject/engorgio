from engordio.signals import Scan, Decompress


def scanner_worker(filepath, scan_queue, decompress_queue, scan_fn):
    for e in scan_fn(filepath):
        if isinstance(e, Scan):
            scan_queue.put(e.path)
        else:
            decompress_queue.put(e.path)
