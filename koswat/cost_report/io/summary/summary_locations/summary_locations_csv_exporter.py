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

import logging
from pathlib import Path

from koswat.core.io.csv.koswat_csv_writer import KoswatCsvWriter
from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_locations.summary_locations_csv_fom_builder import (
    SummaryLocationsCsvFomBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryLocationsCsvExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        if not isinstance(koswat_summary, KoswatSummary):
            raise ValueError("No 'KoswatSummary' object provided.")
        if not isinstance(export_path, Path):
            raise ValueError("No export path location provided.")

        _csv_fom_builder = SummaryLocationsCsvFomBuilder()
        _csv_fom_builder.koswat_summary = koswat_summary
        _csv_fom = _csv_fom_builder.build()
        if not _csv_fom:
            logging.error(
                "Export of %s failed; it was not possible to convert it into csv format.",
                KoswatSummary.__name__,
            )
            return

        if not export_path.parent.is_dir():
            export_path.parent.mkdir(parents=True)
        KoswatCsvWriter().write(_csv_fom, export_path)
