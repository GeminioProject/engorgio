import pytest


@pytest.mark.parametrize('module,name', [
    # Signals
    ('engordio.signals', '_Signal'),
    ('engordio.signals', 'DirFound'),
    ('engordio.signals', 'FileFound'),
    ('engordio.signals', 'SymlinkFound'),
    ('engordio.signals', 'SpecialFileFound'),
    ('engordio.signals', 'UserScanRequested'),
    ('engordio.signals', 'Decompressed'),
    ('engordio.signals', 'DecompressionDiscarded'),
    ('engordio.signals', 'DecompressionFailed'),
    ('engordio.signals', 'ContentAdded'),
])
def test_objects_are_importable(module, name):
    try:
        exec(f'from {module} import {name}')
    except ImportError as exc:
        assert False, exc

