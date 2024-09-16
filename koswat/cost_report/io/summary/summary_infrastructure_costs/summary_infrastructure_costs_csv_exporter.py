from pathlib import Path

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryInfrastructureCostsCsvExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        pass
