import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results
from tests.cost_report.io.csv import valid_mocked_summary


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_matrix_csv_exporter_export(
        self, valid_mocked_summary: KoswatSummary, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        _export_path = _test_dir.joinpath("matrix_results.csv")
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        # 2. Run test
        SummaryMatrixCsvExporter().export(valid_mocked_summary, _export_path)

        # 3. Validate results
        assert _export_path.exists()
        _read_text = _export_path.read_text(encoding="utf-8")
        _expected_text = """;;Profile type;Kistdam;Kwelscherm;Grondmaatregel profiel;Stabiliteitswand
;;Cost per km (€);0.0;8144.4;16288.8;24433.2
;;Reused grass volume (volume / surface):;nan;nan;nan;nan
;;Reused grass volume (cost):;nan;nan;nan;nan
;;Aanleg grass volume (volume / surface):;nan;nan;nan;nan
;;Aanleg grass volume (cost):;nan;nan;nan;nan
;;Aanleg clay volume (volume / surface):;nan;nan;nan;nan
;;Aanleg clay volume (cost):;nan;nan;nan;nan
;;Reused core volume (volume / surface):;nan;nan;nan;nan
;;Reused core volume (cost):;nan;nan;nan;nan
;;Aanleg core volume (volume / surface):;nan;nan;nan;nan
;;Aanleg core volume (cost):;nan;nan;nan;nan
;;Removed material volume (volume / surface):;nan;nan;nan;nan
;;Removed material volume (cost):;nan;nan;nan;nan
;;New grass layer surface (volume / surface):;nan;nan;nan;nan
;;New grass layer surface (cost):;nan;nan;nan;nan
;;New clay layer surface (volume / surface):;nan;nan;nan;nan
;;New clay layer surface (cost):;nan;nan;nan;nan
;;New core layer surface (volume / surface):;nan;nan;nan;nan
;;New core layer surface (cost):;nan;nan;nan;nan
;;New maaiveld surface (volume / surface):;nan;nan;nan;nan
;;New maaiveld surface (cost):;nan;nan;nan;nan
;;Total measure meters;0;1;1;2
;;Total measure cost;0.0;8.1444;16.2888;48.8664;73.2996
A;0.24;0.42;0;1;1;1;Kwelscherm
A;2.4;0.42;0;0;1;1;Grondmaatregel profiel
A;0.24;2.4;0;0;0;1;Stabiliteitswand
A;2.4;2.4;0;0;0;0;Stabiliteitswand"""
        assert _expected_text == _read_text
