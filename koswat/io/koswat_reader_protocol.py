from pathlib import Path
from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.io.file_object_model_protocol import ImportFileObjectModelProtocol


@runtime_checkable
class KoswatReaderProtocol(Protocol):
    def supports_file(self, file_path: Path) -> bool:
        """
        Validates whether the current reader is capable of importing data from the provided file.

        Args:
            file_path (Path): Path to a file that should be imported.

        Returns:
            bool: Result of validation.
        """
        pass

    def read(self, file_path: Path) -> ImportFileObjectModelProtocol:
        """
        Imports the data from the `file_path` into a concrete implementation of a `ImportFileObjectModelProtocol`.

        Args:
            file_path (Path): Path to a file that should be imported.

        Returns:
            ImportFileObjectModelProtocol: Model representing the data in the file.
        """
        pass
