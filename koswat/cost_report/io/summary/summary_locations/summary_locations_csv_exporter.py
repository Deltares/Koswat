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
