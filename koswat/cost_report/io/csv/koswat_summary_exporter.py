from click import Path
from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_locations.summary_locations_csv_exporter import SummaryLocationsCsvExporter
from koswat.cost_report.io.csv.summary_cost.summary_cost_csv_exporter import SummaryCostCsvExporter
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class KoswatSummaryExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        SummaryCostCsvExporter().export(koswat_summary, export_path.joinpath("summary_costs.csv"))
        SummaryLocationsCsvExporter().export(koswat_summary, export_path.joinpath("summary_locations.csv"))