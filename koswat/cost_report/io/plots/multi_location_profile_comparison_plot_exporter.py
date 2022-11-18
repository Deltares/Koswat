from pathlib import Path

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.plots import close_figure, get_plot
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class MultiLocationProfileComparisonPlotExporter(PlotExporterProtocol):
    export_dir: Path

    def export(self, cost_report: MultiLocationProfileCostReport) -> None:
        _fig_filepath = self.export_dir / cost_report.profile_type

        self._comparing_profiles(cost_report, _fig_filepath.with_suffix(".png"))

    def _comparing_profiles(self, profile_report: ProfileCostReport, file_path: Path):
        # Define canvas
        _figure = get_plot(180)
        _subplot = _figure.add_subplot()

        # Create plot builder.
        _list_profile_plot = ListKoswatProfilePlot()
        _list_profile_plot.koswat_object = [
            (
                profile_report.reinforced_profile.old_profile,
                "#03a9fc",
            ),
            (profile_report.reinforced_profile, "#fc0303"),
        ]
        _list_profile_plot.subplot = _subplot
        _list_profile_plot.plot()

        # Export plots
        _figure.savefig(file_path)
        close_figure()
