import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_costs.summary_costs_csv_exporter import (
    SummaryCostsCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results


class TestSummaryCostsCsvExporter:
    def test_initialize(self):
        _exporter = SummaryCostsCsvExporter()
        assert isinstance(_exporter, SummaryCostsCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_cost_csv_exporter_export(
        self, valid_mocked_summary: KoswatSummary, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        _export_path = _test_dir.joinpath("summary_costs_results.csv")
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        # 2. Run test
        SummaryCostsCsvExporter().export(valid_mocked_summary, _export_path)

        # 3. Validate results
        assert _export_path.exists()
        _read_text = _export_path.read_text(encoding="utf-8")
        _expected_text = """Profile type;Kistdam;Kwelscherm;Grondmaatregel profiel;Stabiliteitswand
Strategy reinforcement order;-1;-1;-1;-1
Cost per km (Euro/km);0.0;8144.4;16288.8;24433.2
Cost per km incl surtax (Euro/km);0.0;12216.6;24433.2;36649.8
New grass volume (quantity):;0.0;0.0;0.0;0.0
New grass volume (cost):;0.0;0.0;0.0;0.0
New grass volume (cost incl surtax):;0.0;0.0;0.0;0.0
New clay volume (quantity):;0.0;0.0;0.0;0.0
New clay volume (cost):;0.0;0.0;0.0;0.0
New clay volume (cost incl surtax):;0.0;0.0;0.0;0.0
New core volume (quantity):;0.0;0.0;0.0;0.0
New core volume (cost):;0.0;0.0;0.0;0.0
New core volume (cost incl surtax):;0.0;0.0;0.0;0.0
Reused grass volume (quantity):;0.0;0.0;0.0;0.0
Reused grass volume (cost):;0.0;0.0;0.0;0.0
Reused grass volume (cost incl surtax):;0.0;0.0;0.0;0.0
Reused core volume (quantity):;0.0;0.0;0.0;0.0
Reused core volume (cost):;0.0;0.0;0.0;0.0
Reused core volume (cost incl surtax):;0.0;0.0;0.0;0.0
Removed material volume (quantity):;0.0;0.0;0.0;0.0
Removed material volume (cost):;0.0;0.0;0.0;0.0
Removed material volume (cost incl surtax):;0.0;0.0;0.0;0.0
New grass layer surface (quantity):;0.0;0.0;0.0;0.0
New grass layer surface (cost):;0.0;0.0;0.0;0.0
New grass layer surface (cost incl surtax):;0.0;0.0;0.0;0.0
New clay layer surface (quantity):;0.0;0.0;0.0;0.0
New clay layer surface (cost):;0.0;0.0;0.0;0.0
New clay layer surface (cost incl surtax):;0.0;0.0;0.0;0.0
New core layer surface (quantity):;0.0;0.0;0.0;0.0
New core layer surface (cost):;0.0;0.0;0.0;0.0
New core layer surface (cost incl surtax):;0.0;0.0;0.0;0.0
New ground level surface (quantity):;0.0;0.0;0.0;0.0
New ground level surface (cost):;0.0;0.0;0.0;0.0
New ground level surface (cost incl surtax):;0.0;0.0;0.0;0.0
Land purchase surface (quantity):;0.0;0.0;0.0;0.0
Land purchase surface (cost):;0.0;0.0;0.0;0.0
Land purchase surface (cost incl surtax):;0.0;0.0;0.0;0.0
Construction length (quantity):;0.0;0.0;0.0;0.0
Construction length (cost):;0.0;0.0;0.0;0.0
Construction length (cost incl surtax):;0.0;0.0;0.0;0.0
Total measure meters;0;1;1;2
Total measure cost;0.0;8.14;16.29;48.87;73.3
Total measure cost incl surtax;0.0;12.22;24.43;73.3;109.95
Infrastructure cost;0.0;0.0;0.0;0.0;0.0
Infrastructure cost incl surtax;0.0;0.0;0.0;0.0;0.0
Total cost;0.0;8.14;16.29;48.87;73.3
Total cost incl surtax;0.0;12.22;24.43;73.3;109.95"""
        assert _expected_text == _read_text
