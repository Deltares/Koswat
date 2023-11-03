import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.koswat_summary_exporter import KoswatSummaryExporter
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results
from tests.cost_report.io.summary import valid_mocked_summary


class TestKoswatSummaryExporter:
    def test_initialize(self):
        _exporter = KoswatSummaryExporter()
        assert isinstance(_exporter, KoswatSummaryExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_koswat_summary_exporter_export_given_valid_data(
        self, valid_mocked_summary: KoswatSummary, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        _expected_costs_summary = _test_dir.joinpath("summary_costs.csv")
        _expected_locations_summary = _test_dir.joinpath("summary_locations.csv")

        # 2. Run test
        KoswatSummaryExporter().export(valid_mocked_summary, _test_dir)

        # 3. Validate results
        assert _expected_costs_summary.exists()
        assert len(_expected_costs_summary.read_text().splitlines()) == 42
        assert _expected_locations_summary.exists()
        assert len(_expected_locations_summary.read_text().splitlines()) == 5
