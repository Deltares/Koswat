from pathlib import Path
from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.io.koswat_exporter_protocol import KoswatExporterProtocol


@runtime_checkable
class PlotExporterProtocol(KoswatExporterProtocol, Protocol):
    export_dir: Path

    def export(self) -> None:
        """
        Exports a given object into a plot.
        """
        pass
