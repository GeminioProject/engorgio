from dataclasses import dataclass

import blinker

from engordio.signals import _Signal


def test_signal_dataclass_subclasses_have_blinker_signal():
    @dataclass
    class Dummy(_Signal):
        pass

    obj = Dummy()
    assert hasattr(obj, '_signal'), "Subclass must have '_signal' attr"
    assert isinstance(obj._signal, blinker.base.NamedSignal)


def test_signal_dataclass_subclasses_instances_have_different_signal():
    @dataclass
    class Dummy1(_Signal):
        pass

    @dataclass
    class Dummy2(_Signal):
        pass

    obj1 = Dummy1()
    obj2 = Dummy2()

    assert obj1._signal is not obj2._signal


def test_signal_dataclass_subclass_instances_have_same_signal():
    @dataclass
    class Dummy(_Signal):
        pass

    obj1 = Dummy()
    obj2 = Dummy()

    assert obj1._signal is obj2._signal
