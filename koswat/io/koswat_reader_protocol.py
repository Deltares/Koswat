from pathlib import Path
from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class FileObjectModelProtocol(Protocol):
    pass


@runtime_checkable
class KoswatReaderProtocol(Protocol):
    def read(self, file_path: Path) -> FileObjectModelProtocol:
        pass
