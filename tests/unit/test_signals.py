def test_signal_scan_exists():
    try:
        from engordio.signals import Scan
    except ImportError as exc:
        assert False, exc


def test_signal_decompress_exists():
    try:
        from engordio.signals import Decompress
    except ImportError as exc:
        assert False, exc
