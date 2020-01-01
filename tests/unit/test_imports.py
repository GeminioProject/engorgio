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
    ('engorgio.signals', 'ExitRequested'),
    ('engorgio.signals', 'PathProcessingFinished'),

    # Entity and entity helpers
    ('engorgio.entity', 'Entity'),
    ('engorgio.entity', 'prepare_all'),
    ('engorgio.entity', 'start_all'),
    ('engorgio.entity', 'join_all'),

    # Parse
    ('engorgio.parser', 'make_parser'),

    # Entities
    ('engorgio.entities.scanner', 'Scanner'),
    ('engorgio.entities.stopper', 'Stopper'),
])
def test_objects_are_importable(module, name):
    try:
        exec(f'from {module} import {name}')
    except ImportError as exc:
        assert False, exc
