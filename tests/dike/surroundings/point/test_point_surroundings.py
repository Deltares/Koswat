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

    @pytest.mark.parametrize(
        "zones, surroundings_matrix, expected_values",
        [
            pytest.param(
                ([0, 5], [5, 25]), {30: 0, 35: 5}, [0, 0], id="No infra in zone A or B."
            ),
            pytest.param(
                ([0, 8], [8, 76]),
                {5.0: 0.0, 10.0: 1.0, 20.0: 0.0, 25.0: 1.0},
                [1, 1],
                id="Overlapping distances.",
            ),
        ],
    )
    def test_get_total_infrastructure_per_zone_given_zones_and_surround_matrix(
        self,
        zones: tuple[list[int], list[int]],
        surroundings_matrix: dict[int, int],
        expected_values: list[int],
    ):
        # 1. Define test data.
        _ps = PointSurroundings(surroundings_matrix=surroundings_matrix)

        # 2. Run test.
        _total_infra = _ps.get_total_infrastructure_per_zone(*zones)

        # 3. Verify expectations.
        assert _total_infra == expected_values
