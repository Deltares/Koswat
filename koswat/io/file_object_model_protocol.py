from typing import Any, List, Protocol, runtime_checkable


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
class ExportFileObjectModelProtocol(FileObjectModelProtocol, Protocol):
    def get_lines(self) -> List[Any]:
        """
        Returns all the data from this `ExportFileObjectModelProtocol` as lines.
        Generally used for export functionality.

        Returns:
            List[Any]: Data ordered in lines
        """
        pass


@runtime_checkable
class ImportFileObjectModelProtocol(FileObjectModelProtocol, Protocol):
    pass
