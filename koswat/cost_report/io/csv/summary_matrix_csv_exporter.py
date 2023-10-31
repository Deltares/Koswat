from pathlib import Path

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_cost.summary_cost_csv_exporter import (
    SummaryCostCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryMatrixCsvExporter(KoswatExporterProtocol):
    def export(
        self, koswat_summary: KoswatSummary, export_path: Path, **kwargs
    ) -> None:
        SummaryCostCsvExporter().export(koswat_summary, export_path)
