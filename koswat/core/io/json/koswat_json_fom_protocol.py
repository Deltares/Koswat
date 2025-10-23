from typing import Any, Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatJsonFomProtocol(FileObjectModelProtocol, Protocol):
    file_stem: str
    content: dict[str, Any]

    def is_valid(self) -> bool:
        """
        Validates the current structure of this `KoswatJsonFomProtocol` instance.

        Returns:
            bool: True when is a valid FOM.
        """
        pass
