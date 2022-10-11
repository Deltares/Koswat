from typing import Type

from koswat.calculations import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    ReinforcementProfileProtocol,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.io.koswat_exporter_protocol import KoswatExporterProtocol


class MockSummary(MultiLocationProfileCostReport):
    total_cost = 42000
    total_volume = 24000
    profile_type: str = ""


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)
        assert not _exporter.data_object_model

    def _create_report(
        self, report_type: Type[ReinforcementProfileProtocol]
    ) -> MultiLocationProfileCostReport:
        _report = MockSummary()
        _report.profile_type = str(report_type())
        _report.locations = []
        return _report

    def test_build(self):
        # 1. Define test data.
        _exporter = SummaryMatrixCsvExporter()
        _summary = KoswatSummary()
        _exporter.data_object_model = _summary
        _required_profiles = [
            CofferdamReinforcementProfile,
            PipingWallReinforcementProfile,
            SoilReinforcementProfile,
            StabilityWallReinforcementProfile,
        ]
        _summary.locations_profile_report_list = list(
            map(self._create_report, _required_profiles)
        )

        # 2. Run test
        _matrix_fom = _exporter.build()

        # 3. Verify expectations
        assert isinstance(_matrix_fom, SummaryMatrixCsvFom)
        assert _matrix_fom.is_valid()
