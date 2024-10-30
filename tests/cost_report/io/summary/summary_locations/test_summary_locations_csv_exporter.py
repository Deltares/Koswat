import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_locations.summary_locations_csv_exporter import (
    SummaryLocationsCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results


class TestSummaryLocationsCsvExporter:
    def test_initialize(self):
        _exporter = SummaryLocationsCsvExporter()
        assert isinstance(_exporter, SummaryLocationsCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_locations_csv_exporter_export(
        self, valid_mocked_summary: KoswatSummary, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        _export_path = _test_dir.joinpath("summary_locations.csv")
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        # 2. Run test
        SummaryLocationsCsvExporter().export(valid_mocked_summary, _export_path)

        # 3. Validate results
        assert _export_path.exists()
        _read_text = _export_path.read_text(encoding="utf-8")
        _expected_text = """Section;X coord;Y coord;Kistdam;Kwelscherm;Grondmaatregel profiel;Stabiliteitswand;Ordered selection;Optimized selection
A;0.24;0.42;0;1;1;1;Kwelscherm;Kwelscherm
A;2.4;0.42;0;0;1;1;Grondmaatregel profiel;Grondmaatregel profiel
A;0.24;2.4;0;0;0;1;Stabiliteitswand;Stabiliteitswand
A;2.4;2.4;0;0;0;1;Stabiliteitswand;Stabiliteitswand"""
        assert _expected_text == _read_text
