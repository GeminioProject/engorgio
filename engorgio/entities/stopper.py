from engorgio.entity import Entity
from engorgio.signals import DirFound
from engorgio.signals import ExitRequested
from engorgio.signals import FileFound
from engorgio.signals import PathProcessingFinished
from engorgio.signals import SpecialFileFound
from engorgio.signals import SymlinkFound
from engorgio.signals import UserScanRequested


class Stopper(Entity):
    def _configure(self):
        self.pending = 0
        self.processed = 0

    def _prepare(self):
        self._attach(PathProcessingFinished, self.on_file_processed)
        self._attach(DirFound, self.on_file_discovered)
        self._attach(FileFound, self.on_file_discovered)
        self._attach(SpecialFileFound, self.on_file_discovered)
        self._attach(SymlinkFound, self.on_file_discovered)
        self._attach(UserScanRequested, self.on_file_discovered)

    def on_file_processed(self, signal):
        self.processed += 1
        if self.processed == self.pending:
            ExitRequested().emit()

    def on_file_discovered(self, signal):
        self.pending += 1
