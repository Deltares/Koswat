import math

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


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

    @pytest.mark.parametrize(
        "zone_a_width, zone_b_width, expected_total_widths",
        [
            pytest.param(4, 4, (1.5, 3), id="'A' [0, 4], 'B' [4, 8]"),
            pytest.param(5, 4, (1.5, 3), id="'A' [0, 5], 'B' [5, 9]"),
            pytest.param(4, 10, (1.5, 9), id="'A' [0, 4], 'B' [4, 14]"),
            pytest.param(5, 10, (1.5, 9), id="'A' [0, 5], 'B' [5, 15]"),
            pytest.param(0, 8, (0, 4.5), id="'B' [0, 8]"),
            pytest.param(0, 10, (0, 4.5), id="'B' [0, 10]"),
            pytest.param(0, 12, (0, 10.5), id="'B' [0, 12]"),
        ],
    )
    def test_get_total_infrastructure_per_zone_with_costs_calculator_case(
        self,
        zone_a_width: float,
        zone_b_width: float,
        expected_total_widths: tuple[float, float],
    ):
        pass
