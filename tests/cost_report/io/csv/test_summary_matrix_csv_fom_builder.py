from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_fom_builder import (
    SummaryMatrixCsvFomBuilder,
)
from tests.cost_report.io.csv import get_valid_test_summary


class TestSummaryMatrixCsvFomBuilder:
    def test_initialize(self):
        _builder = SummaryMatrixCsvFomBuilder()
        assert isinstance(_builder, SummaryMatrixCsvFomBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.koswat_summary

    def test_build(self):
        # 1. Define test data.
        _builder = SummaryMatrixCsvFomBuilder()
        _builder.koswat_summary = get_valid_test_summary()

        # 2. Run test
        _matrix_csv_fom = _builder.build()

        # 3. Verify expectations
        assert isinstance(_matrix_csv_fom, KoswatCsvFom)
        assert _matrix_csv_fom.is_valid()
