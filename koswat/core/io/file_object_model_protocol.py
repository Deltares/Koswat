from typing import Protocol, runtime_checkable


@runtime_checkable
class FileObjectModelProtocol(Protocol):
    def is_valid(self) -> bool:
        """
        Verifies if the current object is valid for import / export.

        Returns:
            bool: Result of the validation.
        """
        pass


@runtime_checkable
class ImportFileObjectModelProtocol(FileObjectModelProtocol, Protocol):
    pass
