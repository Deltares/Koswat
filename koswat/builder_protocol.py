from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BuilderProtocol(Protocol):
    def build(self) -> Any:
        """
        Instantiates a concrete object to separate its initalization from the data structure.

        Returns:
            Any: Intance of a created object within Koswat domain.
        """
        pass
