import pytest
from shapely.geometry import Polygon

from koswat.core.geometries.calc_library import get_normalized_polygon_difference


class TestCalcLibrary:
    @pytest.mark.parametrize(
        "left_geom, right_geom, expected_area",
        [
            pytest.param(
                Polygon(
                    [
                        (4.4544, 4.2700000000000005),
                        (9.1644, 4.2700000000000005),
                        (25.77518238993711, -0.2),
                        (23.91715303983229, -0.2),
                        (9.1644, 3.7700000000000005),
                        (4.4544, 3.7700000000000005),
                        (-5.220000000000001, -0.4),
                        (-6.380000000000001, -0.4),
                        (4.4544, 4.2700000000000005),
                    ]
                ),
                Polygon(
                    [
                        (-1.1599999999999997, 1.85),
                        (0.1647841726618707, 1.85),
                        (4.619, 3.77),
                        (9.059, 3.77),
                        (23.812, -0.2),
                        (8.621, -0.2),
                        (0, -0.2),
                        (0, -0.4),
                        (-5.055, -0.4),
                        (-6.379999999999999, -0.4),
                        (-1.1599999999999997, 1.85),
                    ]
                ),
                12.7131,
                id="Polygon without sliver",
            ),
            pytest.param(
                Polygon(
                    [
                        (4.7328, 4.39),
                        (9.4428, 4.39),
                        (26.786429447852754, -0.2),
                        (24.897145194274025, -0.2),
                        (9.4428, 3.8899999999999997),
                        (4.7328, 3.8899999999999997),
                        (-5.22, -0.4),
                        (-6.38, -0.4),
                        (4.7328, 4.39),
                    ]
                ),
                Polygon(
                    [
                        (-1.1599999999999997, 1.85),
                        (0.165, 1.85),
                        (0.1651048951048952, 1.85),
                        (4.898, 3.89),
                        (9.339, 3.89),
                        (24.793, -0.2),
                        (8.621, -0.2),
                        (0, -0.2),
                        (0, -0.4),
                        (-5.055, -0.4),
                        (-6.379999999999999, -0.4),
                        (-1.1599999999999997, 1.85),
                    ]
                ),
                13.2109,
                id="Polygon with sliver",
            ),
        ],
    )
    def test_get_normalized_polygon_difference_returns_polygon(
        self, left_geom: Polygon, right_geom: Polygon, expected_area: float
    ):
        # 1. Define test data

        # 2. Execute test
        _result_geom = get_normalized_polygon_difference(left_geom, right_geom)

        # 3. Verify results
        assert isinstance(_result_geom, Polygon)
        assert _result_geom.area == pytest.approx(expected_area, rel=1e-4)
