import pytest


@pytest.mark.parametrize('module,name', [
    # Signals
    ('engorgio.signals', '_Signal'),
    ('engorgio.signals', 'DirFound'),
    ('engorgio.signals', 'FileFound'),
    ('engorgio.signals', 'SymlinkFound'),
    ('engorgio.signals', 'SpecialFileFound'),
    ('engorgio.signals', 'UserScanRequested'),
    ('engorgio.signals', 'Decompressed'),
    ('engorgio.signals', 'DecompressionDiscarded'),
    ('engorgio.signals', 'DecompressionFailed'),
    ('engorgio.signals', 'ContentAdded'),

    # Entities
    ('engorgio.entity', 'Entity'),
])
def test_objects_are_importable(module, name):
    try:
        exec(f'from {module} import {name}')
    except ImportError as exc:
        assert False, exc
