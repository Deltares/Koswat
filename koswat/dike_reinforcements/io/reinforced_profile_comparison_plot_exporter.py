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

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class ReinforcedProfileComparisonPlotExporter(PlotExporterProtocol):
    export_dir: Path
    reinforced_profile: ReinforcementProfileProtocol

    def export(self) -> None:
        _section_name = self.reinforced_profile.old_profile.input_data.dike_section
        self.export_dir.mkdir(parents=True, exist_ok=True)
        _file_path = self.export_dir.joinpath(
            f"{_section_name}_{self.reinforced_profile}"
        ).with_suffix(".png")

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
