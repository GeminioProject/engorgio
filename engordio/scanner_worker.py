def scanner_worker(scan_queue, decompress_queue, scan_fn):
    list(scan_fn(scan_queue.get()))
