from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class FileObjectModelProtocol(Protocol):
    def is_valid(self) -> bool:
        pass
