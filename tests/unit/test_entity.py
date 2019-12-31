import pytest
import inspect

from engorgio.entity import Entity


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
                                  'join'])
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
