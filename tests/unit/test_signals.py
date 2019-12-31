from dataclasses import dataclass

import blinker
import pytest

from engordio import signals


def test_signal_dataclass_subclasses_have_blinker_signal():
    @dataclass
    class Dummy(signals._Signal):
        pass

    obj = Dummy()
    assert hasattr(obj, '_signal'), "Subclass must have '_signal' attr"
    assert isinstance(obj._signal, blinker.base.NamedSignal)


def test_signal_dataclass_subclasses_instances_have_different_signal():
    @dataclass
    class Dummy1(signals._Signal):
        pass

    @dataclass
    class Dummy2(signals._Signal):
        pass

    obj1 = Dummy1()
    obj2 = Dummy2()

    assert obj1._signal is not obj2._signal


def test_signal_dataclass_subclass_instances_have_same_signal():
    @dataclass
    class Dummy(signals._Signal):
        pass

    obj1 = Dummy()
    obj2 = Dummy()

    assert obj1._signal is obj2._signal


@pytest.mark.parametrize('cls',
                         [signals.DirFound,
                          signals.FileFound,
                          signals.UserScanRequested,
                          signals.Decompressed,
                          signals.DecompressionDiscarded,
                          signals.DecompressionFailed,
                          signals.ContentAdded])
def test_signals_are_subclass_of_signal_base_class(cls):
    assert issubclass(cls, signals._Signal)


def test_signal_subclass_has_connect():
    class Dummy(signals._Signal):
        pass

    assert hasattr(Dummy(), 'connect')


def test_signal_connect_does_connect_to_signal():
    class Dummy(signals._Signal):
        pass

    def handler(sender, signal):
        return signal
    Dummy.connect(handler)
    obj = Dummy()

    res = obj._signal.send(signal=obj)

    assert res[0][1] is obj


def test_signal_subclass_has_emit():
    class Dummy(signals._Signal):
        pass

    assert hasattr(Dummy(), 'emit')


def test_signal_emit_send_signal_to_connected_handler():
    class Dummy(signals._Signal):
        pass
    sent = None

    def handler(sender, signal):
        nonlocal sent
        sent = signal
    Dummy.connect(handler)
    obj = Dummy()

    obj.emit()

    assert sent is obj
