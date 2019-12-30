from engordio.signals import DirFound, FileFound


def dispatch_signals(scan_queue, decompress_queue, signals):
    for s in signals:
        if isinstance(s, DirFound):
            scan_queue.put(s.path)
        elif isinstance(s, FileFound):
            decompress_queue.put(s.path)
        else:
            raise ValueError(f'Unknown signal {s!r}')
