"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
