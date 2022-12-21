from pathlib import Path
from typing import Protocol

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatWriterProtocol(Protocol):
    def write(self, fom_instance: FileObjectModelProtocol, to_path: Path) -> None:
        pass