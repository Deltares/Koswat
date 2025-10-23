from pathlib import Path
from typing import Protocol, runtime_checkable

from koswat.core.protocols.data_object_model_protocol import DataObjectModelProtocol


@runtime_checkable
class KoswatImporterProtocol(Protocol):
    def import_from(
        self, from_path: Path
    ) -> DataObjectModelProtocol | list[DataObjectModelProtocol]:
        """
        Generates a valid instance of a `DataObjectModelProtocol` based on the contents from the provided path.

        Args:
            from_path (Path): Path containing data to be read (file or directory).

        Returns:
            DataObjectModelProtocol | list[DataObjectModelProtocol]: Either a single __valid__ instance of a `DataObjectModelProtocol` or a list of them.
        """
        pass
