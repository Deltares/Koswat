from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.io.summary.summary_costs.summary_costs_csv_fom_builder import (
    SummaryCostsCsvFomBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class TestSummaryCostCsvFomBuilder:
    def test_initialize(self):
        _builder = SummaryCostsCsvFomBuilder()
        assert isinstance(_builder, SummaryCostsCsvFomBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.koswat_summary

    def test_build(self, valid_mocked_summary: KoswatSummary):
        # 1. Define test data.
        _builder = SummaryCostsCsvFomBuilder()
        _builder.koswat_summary = valid_mocked_summary

        # 2. Run test
        _matrix_csv_fom = _builder.build()

        # 3. Verify expectations
        assert isinstance(_matrix_csv_fom, KoswatCsvFom)
        assert _matrix_csv_fom.is_valid()
