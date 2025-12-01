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

import logging
from pathlib import Path

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_costs.summary_costs_csv_exporter import (
    SummaryCostsCsvExporter,
)
from koswat.cost_report.io.summary.summary_infrastructure_costs.summary_infrastructure_costs_csv_exporter import (
    SummaryInfrastructureCostsCsvExporter,
)
from koswat.cost_report.io.summary.summary_locations.summary_locations_csv_exporter import (
    SummaryLocationsCsvExporter,
)
from koswat.cost_report.io.summary.summary_locations.summary_locations_shp_exporter import (
    SummaryLocationsShpExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class KoswatSummaryExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        SummaryCostsCsvExporter().export(
            koswat_summary, export_path.joinpath("summary_costs.csv")
        )
        SummaryInfrastructureCostsCsvExporter().export(
            koswat_summary, export_path.joinpath("summary_infrastructure_costs.csv")
        )
        SummaryLocationsCsvExporter().export(
            koswat_summary, export_path.joinpath("summary_locations.csv")
        )
        try:
            SummaryLocationsShpExporter().export(
                koswat_summary, export_path.joinpath("summary_locations")
            )
        except:
            logging.error(
                "Shapefile error!: %s",
                export_path._str,
            )
