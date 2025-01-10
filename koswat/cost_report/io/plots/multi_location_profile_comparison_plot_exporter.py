from pathlib import Path

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike_reinforcements.io.reinforced_profile_comparison_plot_exporter import (
    ReinforcedProfileComparisonPlotExporter,
)
from koswat.dike_reinforcements.io.reinforced_profile_plot_exporter import (
    ReinforcedProfilePlotExporter,
)
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class MultiLocationProfileComparisonPlotExporter(PlotExporterProtocol):
    export_dir: Path
    cost_report: MultiLocationProfileCostReport

    def export(self) -> None:
        # Plot comparison
        _comparison_exporter = ReinforcedProfileComparisonPlotExporter()
        _comparison_exporter.export_dir = self.export_dir
        _comparison_exporter.reinforced_profile = (
            self.cost_report.profile_cost_report.reinforced_profile
        )
        _comparison_exporter.export()

        # Layer breakdown
        _layers_exporter = ReinforcedProfilePlotExporter()
        _layers_exporter.export_dir = self.export_dir
        _layers_exporter.reinforced_profile = (
            self.cost_report.profile_cost_report.reinforced_profile
        )
        _layers_exporter.export()
