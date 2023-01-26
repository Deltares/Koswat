import shutil

import pytest

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results
from tests.cost_report.io.csv import get_valid_test_summary


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_matrix_csv_exporter_export(self, request: pytest.FixtureRequest):
        # 1. Define test data.
        _test_dir = test_results / request.node.name
        _export_path = _test_dir / "matrix_results.csv"
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        _fom_summary = get_valid_test_summary()

        # 2. Run test
        SummaryMatrixCsvExporter().export(_fom_summary, _export_path)

        # 3. Validate results
        assert _export_path.exists()
        _read_text = _export_path.read_text()
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
A;0.24;0.42;0;1;1;1
A;2.4;0.42;0;0;1;1
A;0.24;2.4;0;0;0;1
A;2.4;2.4;0;0;0;0"""
        assert _expected_text == _read_text
