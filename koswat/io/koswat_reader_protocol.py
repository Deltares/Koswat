from pathlib import Path
from typing import Any, Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class KoswatReaderProtocol(Protocol):
    def read(self, file_path: Path) -> Any:
        pass
