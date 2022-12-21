import random
from typing import List, Type

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


def _create_locations(locations: int) -> List[PointSurroundings]:
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


def get_valid_test_summary() -> KoswatSummary:
    _required_profiles = [
        CofferdamReinforcementProfile,
        PipingWallReinforcementProfile,
        SoilReinforcementProfile,
        StabilityWallReinforcementProfile,
    ]
    _available_points = _create_locations(len(_required_profiles))
    _summary = KoswatSummary()
    _summary.locations_profile_report_list = list(
        map(lambda x: _create_report(x, _available_points), _required_profiles)
    )
    return _summary
