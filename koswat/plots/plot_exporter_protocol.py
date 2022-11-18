from pathlib import Path
from typing import Any

from koswat.io.koswat_exporter_protocol import KoswatExporterProtocol


class PlotExporterProtocol(KoswatExporterProtocol):
    export_dir: Path

    def export(self, plot_object_model: Any) -> None:
        """
        Exports the given `plot_object_model` into a concrete file format.

        Args:
            plot_object_model (Any): Model containing data to be exported into a plot.
        """
        pass
