import random
from typing import List, Tuple, Type

from shapely.geometry import Point

from koswat.calculations.outside_slope_reinforcement import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.calculations.standard_reinforcement import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class MockSummary(MultiLocationProfileCostReport):
    total_cost = 42000
    profile_type: str = ""
    cost_per_km = 42


class MockLayerReport:
    material = ""
    total_volume = 42


def _create_locations() -> List[PointSurroundings]:
    _points = [(0.24, 0.42), (2.4, 0.42), (0.24, 2.4), (0.24, 2.4)]

    def to_point(tuple_float: Tuple[float, float]) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = Point(tuple_float[0], tuple_float[1])
        _ps.section = "A"
        return _ps

    return list(map(to_point, _points))


def _create_report(
    report_type: Type[ReinforcementProfileProtocol],
    available_points: List[PointSurroundings],
    selected_locations: int,
) -> MultiLocationProfileCostReport:
    def _get_layer(material: str, volume: float) -> MockLayerReport:
        _layer_report = MockLayerReport()
        _layer_report.material = material
        _layer_report.total_volume = volume
        return _layer_report

    _report = MockSummary()
    _report.locations = available_points[0:selected_locations]
    _required_klei = 2.4 * selected_locations
    _required_zand = 4.2 * selected_locations
    _report.profile_type = str(report_type())
    _report.cost_per_km = (_required_klei + _required_zand) * 1234
    _report.profile_cost_report = ProfileCostReport()
    _report.profile_cost_report.layer_cost_reports = [
        _get_layer("Klei", _required_klei),
        _get_layer("Zand", _required_zand),
    ]
    return _report


def get_valid_test_summary() -> KoswatSummary:
    _required_profiles = [
        CofferdamReinforcementProfile,
        PipingWallReinforcementProfile,
        SoilReinforcementProfile,
        StabilityWallReinforcementProfile,
    ]
    _available_points = _create_locations()
    _summary = KoswatSummary()
    _summary.locations_profile_report_list = list(
        map(
            lambda x: _create_report(x, _available_points, _required_profiles.index(x)),
            _required_profiles,
        )
    )
    return _summary
