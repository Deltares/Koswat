import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_locations.summary_locations_shp_exporter import (
    SummaryLocationsShpExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results


class TestSummaryLocationsShpExporter:
    def test_initialize(self):
        _exporter = SummaryLocationsShpExporter()
        assert isinstance(_exporter, SummaryLocationsShpExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_locations_shp_exporter_export(
        self,
        valid_clusters_mocked_summary: KoswatSummary,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        # 2. Run test.
        SummaryLocationsShpExporter().export(valid_clusters_mocked_summary, _test_dir)

        # 3. Verify expectations.
        assert _test_dir.exists()
        _shp_files = list(_test_dir.glob("*.shp"))
        assert len(_shp_files) == 4
