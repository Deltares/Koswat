from click import Path

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
