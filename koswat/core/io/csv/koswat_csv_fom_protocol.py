from typing import List, Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatCsvFomProtocol(FileObjectModelProtocol, Protocol):
    headers: List[str]
    entries: List[List[str]]

    def is_valid(self) -> bool:
        """
        Validates the current structure of this `KoswatCsvFomProtocol` instance.

        Returns:
            bool: True when is a valid FOM.
        """
        pass
