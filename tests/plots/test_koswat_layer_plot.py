import pytest
from numpy import testing
from shapely.geometry import LineString, MultiLineString

from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot

_coordinates = [(0, 0), (0, 2), (2, 2), (2, 0)]


class TestKoswatLayerPlot:
    @pytest.mark.parametrize(
        "valid_geometry",
        [
            pytest.param(LineString(_coordinates), id="From LineString"),
            pytest.param(
                MultiLineString([_coordinates[:2], _coordinates[2:]]),
                id="From MultiLineString",
            ),
        ],
    )
    def test_get_xy_line_coords_from_valid_geometry_returns_tuple(
        self, valid_geometry: LineString | MultiLineString
    ):
        # 1. Define test data.
        assert valid_geometry.is_valid
        _expected_x_coords, _expected_y_coords = zip(*_coordinates)

        # 2. Run test.
        _x_y_coordinates = KoswatLayerPlot._get_xy_line_coords(valid_geometry)

        # 3. Verify expectations.
        assert isinstance(_x_y_coordinates, tuple)
        testing.assert_array_equal(_x_y_coordinates[0], _expected_x_coords)
        testing.assert_array_equal(_x_y_coordinates[1], _expected_y_coords)
