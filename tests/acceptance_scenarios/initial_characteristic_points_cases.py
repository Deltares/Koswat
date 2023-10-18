import pytest
from shapely.geometry.point import Point

from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class InitialPointsLookup(CasesProtocol):
    default = [
        Point(-18.0, 0.0),
        Point(-18.0, 0.0),
        Point(-18.0, 0.0),
        Point(0.0, 6.0),
        Point(5.0, 6.0),
        Point(23.0, 0.0),
        Point(23.0, 0.0),
        Point(23.0, 0.0),
    ]
    calc_profile_scenario_2 = [
        Point(-24, 0),
        Point(-24, 0),
        Point(-24, 0),
        Point(2, 6.5),
        Point(7, 6.5),
        Point(28.60, 2.6),
        Point(82.60, 2.6),
        Point(97, 0),
    ]
    cases = [
        pytest.param(default, id="Default initial profile."),
        pytest.param(calc_profile_scenario_2, id="Scenario 2 calculated profile."),
    ]
