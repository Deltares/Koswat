from pathlib import Path
from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class FileObjectModelProtocol(Protocol):
    def is_valid(self) -> bool:
        pass


@runtime_checkable
class KoswatReaderProtocol(Protocol):
    def supports_file(self, file_path: Path) -> bool:
        pass

    def read(self, file_path: Path) -> FileObjectModelProtocol:
        pass
