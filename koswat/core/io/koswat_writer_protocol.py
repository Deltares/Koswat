from pathlib import Path
from typing import Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatWriterProtocol(Protocol):
    def write(self, fom_instance: FileObjectModelProtocol, to_path: Path) -> None:
        """
        Writes the data from the instance of a `FileObjectModelProtocol` to the `to_path`.

        Args:
            fom_instance (FileObjectModelProtocol): Instance with data to write.
            to_path (Path): Path to file (or directory) where to write the data.
        """
        pass
