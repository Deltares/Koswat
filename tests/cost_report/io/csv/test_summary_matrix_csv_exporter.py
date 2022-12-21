import shutil

import pytest

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from tests import test_results
from tests.cost_report.io.csv import get_valid_test_summary


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_export(self, request: pytest.FixtureRequest):
        # 1. Define test data.
        _test_dir = test_results / request.node.name
        _export_path = _test_dir / "matrix_results.csv"
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        _fom_summary = get_valid_test_summary()
        _expected_result = (
            """a;header\ntwo;entries\nother;more\na;location\nanother;one"""
        )

        # 2. Run test
        SummaryMatrixCsvExporter().export(_fom_summary, _export_path)

        # 3. Validate results
        assert _export_path.exists()
        _written_lines = _export_path.read_text().splitlines(keepends=False)
        assert any(_written_lines)
