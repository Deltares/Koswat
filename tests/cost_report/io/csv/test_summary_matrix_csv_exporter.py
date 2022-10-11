import random
import shutil
from typing import List, Type

import pytest
from shapely.geometry import Point

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
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.koswat_exporter_protocol import KoswatExporterProtocol
from tests import test_results


class MockSummary(MultiLocationProfileCostReport):
    total_cost = 42000
    profile_type: str = ""
    cost_per_km = 42


class MockLayerReport(LayerCostReport):
    material = ""
    total_volume = 42


class TestSummaryMatrixCsvExporter:
    def test_initialize(self):
        _exporter = SummaryMatrixCsvExporter()
        assert isinstance(_exporter, SummaryMatrixCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)
        assert not _exporter.data_object_model

    def _create_locations(self, locations: int) -> List[PointSurroundings]:
        _points = []
        for _ in range(0, locations):
            _x_coord = random.uniform(0, 4).__round__(2)
            _y_coord = random.uniform(0, 4).__round__(2)
            _ps = PointSurroundings()
            _ps.location = Point(_x_coord, _y_coord)
            _ps.section = "A"
            _points.append(_ps)
        return _points

    def _create_report(
        self,
        report_type: Type[ReinforcementProfileProtocol],
        available_points: List[PointSurroundings],
    ) -> MultiLocationProfileCostReport:
        def _get_layer(material: str, volume: float) -> MockLayerReport:
            _layer_report = MockLayerReport()
            _layer_report.material = material
            _layer_report.total_volume = volume
            return _layer_report

        _report = MockSummary()
        _sel_locations = random.choice(range(0, len(available_points)))
        _report.locations = random.sample(available_points, k=_sel_locations)
        _required_klei = random.uniform(1, 100).__round__(2) * _sel_locations
        _required_zand = random.uniform(1, 100).__round__(2) * _sel_locations
        _report.profile_type = str(report_type())
        _report.cost_per_km = (_required_klei + _required_zand) * 1234
        _report.profile_cost_report = ProfileCostReport()
        _report.profile_cost_report.layer_cost_reports = [
            _get_layer("Klei", _required_klei),
            _get_layer("Zand", _required_zand),
        ]
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
        _available_points = self._create_locations(len(_required_profiles))
        _summary.locations_profile_report_list = list(
            map(lambda x: self._create_report(x, _available_points), _required_profiles)
        )

        # 2. Run test
        _matrix_fom = _exporter.build()

        # 3. Verify expectations
        assert isinstance(_matrix_fom, SummaryMatrixCsvFom)
        assert _matrix_fom.is_valid()

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
