from typing import Type

import pytest
from shapely.geometry import Point

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class MockSummary(MultiLocationProfileCostReport):
    total_cost = 42000
    total_cost_with_surtax = 63000
    profile_type: str = ""
    cost_per_km = 42
    cost_with_surtax_per_km = 63


class MockLayerReport:
    material = ""
    total_quantity = 42


def _create_locations() -> list[PointSurroundings]:
    _points = [(0.24, 0.42), (2.4, 0.42), (0.24, 2.4), (2.4, 2.4)]

    def to_point(tuple_float: tuple[float, float], order: int) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = Point(tuple_float[0], tuple_float[1])
        _ps.section = "A"
        _ps.traject_order = order
        return _ps

    return list(map(to_point, _points, range(0, 4)))


def _create_report(
    report_type: Type[ReinforcementProfileProtocol],
    available_points: list[PointSurroundings],
    selected_locations: int,
) -> MultiLocationProfileCostReport:
    def _get_layer(material: str, quantity: float) -> MockLayerReport:
        _layer_report = MockLayerReport()
        _layer_report.material = material
        _layer_report.total_quantity = quantity
        return _layer_report

    _report = MockSummary()
    _report.locations = available_points[0:selected_locations]
    _required_klei = 2.4 * selected_locations
    _required_zand = 4.2 * selected_locations
    _report.cost_per_km = (_required_klei + _required_zand) * 1234
    _report.cost_with_surtax_per_km = _report.cost_per_km * 1.5
    _report.profile_cost_report = ProfileCostReport()
    _report.profile_cost_report.reinforced_profile = report_type()
    _report.profile_cost_report.layer_cost_reports = [
        _get_layer("Klei", _required_klei),
        _get_layer("Zand", _required_zand),
    ]
    return _report


def get_locations_reinforcements(
    summary: KoswatSummary, available_locations: list[PointSurroundings]
) -> list[StrategyLocationReinforcement]:
    _matrix = []
    _available_reinforcements = [
        type(_lp_report.profile_cost_report.reinforced_profile)
        for _lp_report in summary.locations_profile_report_list
    ]
    for _location in available_locations:
        _a_measures = list(
            type(_lp_report.profile_cost_report.reinforced_profile)
            for _lp_report in summary.locations_profile_report_list
            if _location in _lp_report.locations
        )
        _selected_measure = _available_reinforcements[-1]
        if any(_a_measures):
            _selected_measure = _a_measures[0]
        _matrix.append(
            StrategyLocationReinforcement(
                location=_location,
                available_measures=_a_measures,
                selected_measure=_selected_measure,
            )
        )
    return _matrix


@pytest.fixture
def valid_mocked_summary() -> KoswatSummary:
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
    _summary.reinforcement_per_locations = get_locations_reinforcements(
        _summary, _available_points
    )
    return _summary
