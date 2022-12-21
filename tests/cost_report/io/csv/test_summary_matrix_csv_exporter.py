import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from tests import test_results


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_export(self, request: pytest.FixtureRequest):
        # 1. Define test data.
        _test_dir = test_results / request.node.name
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        _exporter = SummaryMatrixCsvExporter()
        _exporter.export_filepath = _test_dir / "matrix_results.csv"
        _fom_summary = SummaryMatrixCsvFom()
        _fom_summary.headers = ["a", "header"]
        _fom_summary.cost_rows = [["two", "entries"], ["other", "more"]]
        _fom_summary.location_rows = [["a", "location"], ["another", "one"]]

        _expected_result = (
            """a;header\ntwo;entries\nother;more\na;location\nanother;one"""
        )

        # 2. Run test
        _exporter.export(_fom_summary)

        # 3. Validate results
        assert _exporter.export_filepath.exists()
        _written_text = _exporter.export_filepath.read_text()
        assert _written_text == _expected_result
