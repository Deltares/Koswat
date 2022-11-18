from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class KoswatExporterProtocol(Protocol):

    def export(self, **kwargs) -> None:
        """
        Exports an object model into a concrete file format.
        """
        pass
