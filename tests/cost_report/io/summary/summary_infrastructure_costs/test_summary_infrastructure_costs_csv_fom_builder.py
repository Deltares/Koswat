from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.io.summary.summary_infrastructure_costs.summary_infrastructure_costs_csv_fom_builder import (
    SummaryInfrastructureCostsCsvFomBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests.cost_report.io.summary import valid_mocked_summary


class TestSummaryInfrastructureCostsCsvFomBuilder:
    def test_initialize(self):
        _builder = SummaryInfrastructureCostsCsvFomBuilder()
        assert isinstance(_builder, SummaryInfrastructureCostsCsvFomBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.koswat_summary

    def test_build(self, valid_mocked_summary: KoswatSummary):
        # 1. Define test data.
        _builder = SummaryInfrastructureCostsCsvFomBuilder()
        _builder.koswat_summary = valid_mocked_summary

        # 2. Run test
        _csv_fom = _builder.build()

        # 3. Verify expectations
        assert isinstance(_csv_fom, KoswatCsvFom)
        assert _csv_fom.is_valid()
