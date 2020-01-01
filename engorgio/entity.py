from collections import defaultdict
from enum import Enum, auto
import abc
import queue
import threading

from engorgio.signals import ExitRequested


class _State(Enum):
    """Stated used by the `Entity` internal state machine."""
    INIT = auto()
    PREPARED = auto()
    STARTED = auto()
    JOINED = auto()


class Entity(abc.ABC):
    """
    Encapsulate some functionality in a concurrent execution unit.

    Enforces a protocol to normalize how it is used.

    At instantiation time `_configure` will be called to let the
    subclass set any attributes with values based on `self.config`.

    After that the methods `prepare`, `start` and `join` have to be
    called in that exact order.  Any other order will result in a
    `RuntimeException`.

    """
    def __init__(self, config):
        self.config = config
        self._state = _State.INIT
        self._attached = defaultdict(set)
        self._queue = queue.Queue()
        self._thread = None
        self._configure()

    @abc.abstractmethod
    def _configure(self):  # pragma: no cover
        """Set any attributes needed by the subclass."""
        pass

    @abc.abstractmethod
    def _prepare(self):  # pragma: no cover
        """Attach handlers to needed signals using `self._attach`."""
        pass

    def prepare(self):
        """Call `_prepare`."""
        if self._state is not _State.INIT:
            raise RuntimeError(
                f'Cannot prepare() when state is {self._state.name}')
        self._state = _State.PREPARED
        ExitRequested.connect(self._enqueue)
        self._prepare()

    def start(self):
        """
        Start `self._dequeue` in a new thread referenced by `self._thread`.

        """
        if self._state is not _State.PREPARED:
            raise RuntimeError(
                f'Cannot start() when state is {self._state.name}')
        self._state = _State.STARTED
        self._thread = threading.Thread(group=None, target=self._dequeue)
        self._thread.start()

    def join(self):
        """
        Wait for `self._thread` to finish.

        """
        if self._state is not _State.STARTED:
            raise RuntimeError(
                f'Cannot join() when state is {self._state.name}')
        self._thread.join()
        self._state = _State.JOINED

    def _attach(self, signal, handler):
        """
        Arrange that `handler` be called when `signal` arrives.

        """
        if signal not in self._attached:
            signal.connect(self._enqueue)
        self._attached[signal].add(handler)

    def _dispatch(self, signal):
        """
        Call all handlers attached by `self._attach` to `signal`.

        """
        for handler in self._attached[signal.__class__]:
            handler(signal)

    def _dequeue(self):
        """
        Dequeue from `self._queue` until an `ExitRequested` arrives.

        This function is executed in a separate thread.

        """
        while True:
            signal = self._queue.get()
            self._dispatch(signal)
            if isinstance(signal, ExitRequested):
                break

    def _enqueue(self, sender, signal):
        """
        Add the given signal to `self._queue` to be processed by the handlers.

        This is the handler given to `engordio.signals` signals.

        Is called in the main application thread.

        """
        self._queue.put(signal)


def prepare_all(*entities):
    """Prepare all given entities."""
    for entity in entities:
        entity.prepare()


def start_all(*entities):
    """Start all given entities."""
    for entity in entities:
        entity.start()


def join_all(*entities):
    """Join all given entities."""
    for entity in entities:
        entity.join()
