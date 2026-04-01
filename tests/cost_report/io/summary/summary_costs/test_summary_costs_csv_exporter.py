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
        _expected_text = "Profile type;Kistdam;Kwelscherm;Grondmaatregel profiel;Stabiliteitswand kruin;Stabiliteitswand teen\n\
Strategy reinforcement order;-1;-1;-1;-1;-1\n\
Cost per km (Euro/km);0.0;8144.4;16288.8;24433.2;32577.6\n\
Cost per km incl surtax (Euro/km);0.0;12216.6;24433.2;36649.8;48866.4\n\
New grass volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New grass volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
New grass volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New clay volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New clay volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
New clay volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New core volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New core volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
New core volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Reused grass volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
Reused grass volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
Reused grass volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Reused core volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
Reused core volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
Reused core volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Removed material volume (quantity):;0.0;0.0;0.0;0.0;0.0\n\
Removed material volume (cost):;0.0;0.0;0.0;0.0;0.0\n\
Removed material volume (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New grass layer surface (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New grass layer surface (cost):;0.0;0.0;0.0;0.0;0.0\n\
New grass layer surface (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New clay layer surface (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New clay layer surface (cost):;0.0;0.0;0.0;0.0;0.0\n\
New clay layer surface (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New core layer surface (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New core layer surface (cost):;0.0;0.0;0.0;0.0;0.0\n\
New core layer surface (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
New ground level surface (quantity):;0.0;0.0;0.0;0.0;0.0\n\
New ground level surface (cost):;0.0;0.0;0.0;0.0;0.0\n\
New ground level surface (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Land purchase surface (quantity):;0.0;0.0;0.0;0.0;0.0\n\
Land purchase surface (cost):;0.0;0.0;0.0;0.0;0.0\n\
Land purchase surface (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Construction length (quantity):;0.0;0.0;0.0;0.0;0.0\n\
Construction length (cost):;0.0;0.0;0.0;0.0;0.0\n\
Construction length (cost incl surtax):;0.0;0.0;0.0;0.0;0.0\n\
Total measure meters;0;1;1;1;1\n\
Total measure cost;0.0;8.14;16.29;24.43;32.58;81.44\n\
Total measure cost incl surtax;0.0;12.22;24.43;36.65;48.87;122.17\n\
Infrastructure cost;0.0;0.0;0.0;0.0;0.0;0.0\n\
Infrastructure cost incl surtax;0.0;0.0;0.0;0.0;0.0;0.0\n\
Total cost;0.0;8.14;16.29;24.43;32.58;81.44\n\
Total cost incl surtax;0.0;12.22;24.43;36.65;48.87;122.17"
        assert _expected_text == _read_text
