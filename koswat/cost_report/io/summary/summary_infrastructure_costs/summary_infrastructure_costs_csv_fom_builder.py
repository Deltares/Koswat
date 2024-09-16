from collections import defaultdict

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryInfrastructureCostsCsvFomBuilder(BuilderProtocol):
    koswat_summary: KoswatSummary

    def __init__(self) -> None:
        self.koswat_summary = None

    def build(self) -> KoswatCsvFom:
        _csv_fom = KoswatCsvFom()

        _dict_of_entries = defaultdict(list)

        return _csv_fom
