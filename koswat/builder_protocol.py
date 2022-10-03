from typing import Any, Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class BuilderProtocol(Protocol):
    def build(self) -> Any:
        pass
