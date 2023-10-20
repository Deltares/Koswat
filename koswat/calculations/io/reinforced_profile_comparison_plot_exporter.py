from pathlib import Path

from koswat.calculations.reinforcement_profiles.reinforcement_profile_protocol import ReinforcementProfileProtocol
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class ReinforcedProfileComparisonPlotExporter(PlotExporterProtocol):
    export_dir: Path
    reinforced_profile: ReinforcementProfileProtocol

    def export(self) -> None:
        self.export_dir.mkdir(parents=True, exist_ok=True)
        _file_path = (self.export_dir / str(self.reinforced_profile)).with_suffix(
            ".png"
        )

        # Define canvas
        with KoswatFigureContextHandler(_file_path, 180) as _koswat_figure:
            _subplot = _koswat_figure.add_subplot()

            # Create plot builder.
            _list_profile_plot = ListKoswatProfilePlot()
            _list_profile_plot.koswat_object = [
                (
                    self.reinforced_profile.old_profile,
                    "#03a9fc",
                ),
                (self.reinforced_profile, "#fc0303"),
            ]
            _list_profile_plot.subplot = _subplot
            _list_profile_plot.plot()
