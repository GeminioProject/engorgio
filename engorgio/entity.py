import abc
from enum import Enum, auto


class _State(Enum):
    INIT = auto()
    PREPARED = auto()
    STARTED = auto()
    JOINED = auto()


class Entity(abc.ABC):
    """
    Encapsulate some functionality in a, usually concurrent, execution
    unit.

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
        self._configure()

    @abc.abstractmethod
    def _configure(self):
        """Set any attributes needed by the subclass."""
        pass

    @abc.abstractmethod
    def _prepare(self):
        """Attach handlers to needed signals."""
        pass

    def prepare(self):
        """Call `_prepare`."""
        if self._state is not _State.INIT:
            raise RuntimeError(f'Cannot prepare from state {self._state}')
        self._state = _State.PREPARED
        self._prepare()

    def start(self):
        if self._state is not _State.PREPARED:
            raise RuntimeError(f'Cannot start from state {self._state}')
        self._state = _State.STARTED

    def join(self):
        if self._state is not _State.STARTED:
            raise RuntimeError(f'Cannot join from state {self._state}')
        self._state = _State.JOINED
