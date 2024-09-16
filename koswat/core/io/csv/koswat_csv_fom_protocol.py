from typing import Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatCsvFomProtocol(FileObjectModelProtocol, Protocol):
    headers: list[str] | list[list[str]]
    entries: list[list[str]]

    def is_valid(self) -> bool:
        """
        Validates the current structure of this `KoswatCsvFomProtocol` instance.

        Returns:
            bool: True when is a valid FOM.
        """
        pass
