"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_locations.cluster_collection_shp_fom import (
    ClusterCollectionShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryLocationsShpExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        if not export_path.exists():
            export_path.mkdir(parents=True)
        _measures = export_path.joinpath("summary_locations_measures.shp")
        _old = export_path.joinpath("summary_locations_old.shp")
        _new = export_path.joinpath("summary_locations_new.shp")

        # Get clusters comparing old to new.
        _clusters = ClusterCollectionShpFom.from_summary(
            koswat_summary, lambda x: x.current_selected_measure
        ).generate_geodataframes()

        if not _clusters.is_valid():
            return

        # Export clusters to file
        _clusters.base_layer.to_file(_measures)
        _clusters.initial_state.to_file(_old)
        _clusters.new_state.to_file(_new)

        # Get clusters for steps
        _step_clusters = ClusterCollectionShpFom.from_summary(
            koswat_summary, lambda x: x.get_selected_measure_steps()[1]
        ).generate_geodataframes()

        if not _step_clusters.is_valid():
            return

        # Export clusters to file
        _step_clusters.new_state.to_file(
            export_path.joinpath("summary_locations_step.shp")
        )
