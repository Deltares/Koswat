from typing import Any, List, Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class FileObjectModelProtocol(Protocol):
    def is_valid(self) -> bool:
        """
        Verifies if the current object is valid for import / export.

        Returns:
            bool: Result of the validation.
        """
        pass

    def get_lines(self) -> List[Any]:
        """
        Returns all the data from this `FileObjectModelProtocol` as lines.

        Returns:
            List[Any]: Data ordered in lines
        """
        pass
