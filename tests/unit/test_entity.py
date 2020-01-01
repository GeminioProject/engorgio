from unittest.mock import MagicMock, patch
import inspect
import threading

import pytest

from engorgio.entity import Entity
from engorgio.entity import join_all
from engorgio.entity import prepare_all
from engorgio.entity import start_all
from engorgio.signals import _Signal, ExitRequested


def test_is_abstract():
    assert inspect.isabstract(Entity)


@pytest.mark.parametrize('name', ['_configure',
                                  '_prepare'])
def test_has_some_abstract_methods(name):
    try:
        method = getattr(Entity, name)
    except AttributeError:
        assert False, f"Method not found: {name}"
    else:
        isabstract = getattr(method, '__isabstractmethod__', None)

    assert isabstract is True, "Not an abstract method"


@pytest.mark.parametrize('name', ['prepare',
                                  'start',
                                  'join',
                                  '_attach',
                                  '_dispatch',
                                  '_dequeue',
                                  '_enqueue'])
def test_has_some_regular_methods(name):
    try:
        method = getattr(Entity, name)
    except AttributeError:
        assert False, f"Method not found: {name}"

    assert inspect.isfunction(method)


def test_store_config():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _prepare(self):
            pass

    config = object()
    entity = Dummy(config)

    assert getattr(entity, 'config', None) is config


def test_call_configure():
    called = False

    class Dummy(Entity):
        def _configure(self):
            nonlocal called
            called = True

        def _prepare(self):
            pass

    Dummy(None)

    assert called


def test_start_should_raise_if_prepare_not_called():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _prepare(self):
            pass

    entity = Dummy(None)

    with pytest.raises(RuntimeError):
        entity.start()


def test_return_none_on_start():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()

    assert entity.start() is None


def test_join_should_raise_if_start_not_called():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _prepare(self):
            pass

    entity = Dummy(None)

    with pytest.raises(RuntimeError):
        entity.join()


def test_return_none_on_join():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _dequeue(self):
            pass  # Avoid infinite loop

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()
    entity.start()

    assert entity.join() is None


def test_raise_if_joined_twice():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _dequeue(self):
            pass  # Avoid infinite loop

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()
    entity.start()
    entity.join()

    with pytest.raises(RuntimeError):
        entity.join()


def test_raise_if_prepare_after_join():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _dequeue(self):
            pass  # Avoid infinite loop

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()
    entity.start()
    entity.join()

    with pytest.raises(RuntimeError):
        entity.prepare()


def test_raise_if_start_after_join():

    class Dummy(Entity):
        def _configure(self):
            pass

        def _dequeue(self):
            pass  # Avoid infinite loop

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()
    entity.start()
    entity.join()

    with pytest.raises(RuntimeError):
        entity.start()


def test_prepare_call_concrete_prepare():
    called = False

    class Dummy(Entity):
        def _configure(self):
            pass

        def _prepare(self):
            nonlocal called
            called = True

    entity = Dummy(None)
    entity.prepare()

    assert called


def test_dispatch_signal_to_attached_handler():
    received = None

    class TestSignal(_Signal):
        pass

    test_signal = TestSignal()

    class Dummy(Entity):
        def _configure(self):
            pass

        def on_TestSignal(self, signal):
            nonlocal received
            received = signal

        def _prepare(self):
            self._attach(TestSignal, self.on_TestSignal)

    entity = Dummy(None)
    entity.prepare()

    entity._dispatch(test_signal)

    assert received is test_signal


def test_dispatch_signal_dont_call_twice():
    received = 0

    class TestSignal(_Signal):
        pass

    test_signal = TestSignal()

    class Dummy(Entity):
        def _configure(self):
            pass

        def on_TestSignal(self, signal):
            nonlocal received
            received += 1

        def _prepare(self):
            self._attach(TestSignal, self.on_TestSignal)
            self._attach(TestSignal, self.on_TestSignal)

    entity = Dummy(None)
    entity.prepare()

    entity._dispatch(test_signal)

    assert received == 1


def test_signal_get_connected_to_queue_put():
    """
    Given that ExitRequested is connected during prepare this test also
    tests this condition.  Sorry mom.

    """

    class TestSignal(_Signal):
        connect = MagicMock()

    class Dummy(Entity):
        _enqueue = MagicMock()

        def _configure(self):
            pass

        def on_foo(self, signal):
            pass

        def _prepare(self):
            self._attach(TestSignal, self.on_foo)
            self._attach(TestSignal, self.on_foo)

    entity = Dummy(None)
    with patch('engorgio.signals.ExitRequested.connect') as exit_connect:
        entity.prepare()
        exit_connect.assert_called_once_with(entity._enqueue)
    TestSignal.connect.assert_called_once_with(entity._enqueue)


def test_start_runs_dequeue_in_a_thread():

    tid = threading.get_ident()

    class Dummy(Entity):
        def _configure(self):
            pass

        def _dequeue(self):
            nonlocal tid
            tid = threading.get_ident()

        def _prepare(self):
            pass

    entity = Dummy(None)
    entity.prepare()
    entity.start()
    entity.join()

    assert tid != threading.get_ident()


def test_signals_get_dispatched_until_exitrequested():

    expected = None

    class TestSignal(_Signal):
        pass

    test_signal = TestSignal()

    class Dummy(Entity):
        def _configure(self):
            pass

        def on_TestSignal(self, signal):
            nonlocal expected
            expected = signal

        def _prepare(self):
            self._attach(TestSignal, self.on_TestSignal)

    entity = Dummy(None)
    entity.prepare()
    entity.start()
    test_signal.emit()
    ExitRequested().emit()
    entity.join()

    assert expected is test_signal


def test_prepare_all_call_prepare_on_all_entitities():
    e1 = MagicMock()
    e2 = MagicMock()

    prepare_all(e1, e2)

    e1.prepare.assert_called_once()
    e2.prepare.assert_called_once()


def test_start_all_call_start_on_all_entitities():
    e1 = MagicMock()
    e2 = MagicMock()

    start_all(e1, e2)

    e1.start.assert_called_once()
    e2.start.assert_called_once()


def test_join_all_call_join_on_all_entitities():
    e1 = MagicMock()
    e2 = MagicMock()

    join_all(e1, e2)

    e1.join.assert_called_once()
    e2.join.assert_called_once()
