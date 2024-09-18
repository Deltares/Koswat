import math
from typing import Callable

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from tests.conftest import PointSurroundingsTestCase


class TestPointSurroundings:
    def test_initialize_point_surroundings(self):
        _p_s = PointSurroundings()
        assert isinstance(_p_s, PointSurroundings)
        assert not _p_s.section
        assert not _p_s.location
        assert not _p_s.surroundings_matrix
        assert math.isnan(_p_s.closest_obstacle)

    def test_closest_building_returns_min_value(self):
        _p_s = PointSurroundings()
        _p_s.surroundings_matrix = {42: 1, 24: 1, 2.4: 0}
        assert _p_s.closest_obstacle == 24

    def test_get_total_infrastructure_per_zone_with_costs_calculator_case(
        self,
        point_surroundings_for_zones_builder_fixture: tuple[
            Callable[[], PointSurroundings], PointSurroundingsTestCase
        ],
    ):
        # 1. Define test data.
        (
            _point_surroundings_builder,
            _point_surroundings_case,
        ) = point_surroundings_for_zones_builder_fixture
        _ps = _point_surroundings_builder()
        assert isinstance(_ps, PointSurroundings)

        # 2. Run test.
        _result = _ps.get_total_infrastructure_per_zone(
            _point_surroundings_case.zone_a_limits,
            _point_surroundings_case.zone_b_limits,
        )

        # 3. Verify expectations.
        assert _result == _point_surroundings_case.expected_total_widths
