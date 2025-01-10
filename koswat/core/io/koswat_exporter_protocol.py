from typing import Protocol, runtime_checkable


@runtime_checkable
class KoswatExporterProtocol(Protocol):
    def export(self, **kwargs) -> None:
        """
        Exports an object model into a concrete file format.
        """
        pass
