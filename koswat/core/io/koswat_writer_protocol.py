from pathlib import Path
from typing import Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatWriterProtocol(Protocol):
    def write(self, fom_instance: FileObjectModelProtocol, to_path: Path) -> None:
        pass
