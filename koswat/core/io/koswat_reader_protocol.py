from __future__ import annotations

from pathlib import Path
from typing import Protocol, Type, runtime_checkable

from koswat.core.io.file_object_model_protocol import ImportFileObjectModelProtocol
from koswat.core.protocols import BuilderProtocol


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

    @classmethod
    def with_builder_type(
        cls, builder_type: Type[BuilderProtocol]
    ) -> KoswatReaderProtocol:
        """
        Returns an instance of a `KoswatReaderProtocol` with an attached `BuilderProtocol` type that generates a `ImportFileObjectModelProtocol`.

        Args:
            builder_type (BuilderProtocol): Builder type to use to generate an instance of a `ImportFileObjectModelprotocol`.

        Returns:
            KoswatReaderProtocol: Valid instance of a `KoswatReaderProtocol`.
        """
        pass
