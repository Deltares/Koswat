import pytest
from matplotlib import pyplot
from numpy import testing
from shapely.geometry import LineString, MultiPolygon, Polygon

from koswat.dike.layers.base_layer.koswat_base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_coating_layer import (
    ReinforcementCoatingLayer,
)
from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot

_coordinates = [(0, 0), (0, 2), (2, 2), (2, 0)]


class TestKoswatLayerPlot:
    def test_when_get_xy_line_coords_given_valid_geometry_then_returns_tuple(self):
        # 1. Define test data.
        _geometry = LineString(_coordinates)
        assert _geometry.is_valid
        _expected_x_coords, _expected_y_coords = zip(*_geometry.coords)

        # 2. Run test.
        _x_y_coordinates = KoswatLayerPlot._get_xy_line_coords(_geometry)

        # 3. Verify expectations.
        assert isinstance(_x_y_coordinates, tuple)
        testing.assert_array_equal(_x_y_coordinates[0], _expected_x_coords)
        testing.assert_array_equal(_x_y_coordinates[1], _expected_y_coords)

    def test_when_plot_given_koswat_geometry_then_returns_axes(self):
        # 1. Define test data.
        _geometry = Polygon(_coordinates)
        assert _geometry.is_valid

        _object = KoswatBaseLayer()
        _object.material_type = KoswatMaterialType.SAND
        _object.upper_points = _geometry.boundary
        _object.outer_geometry = _geometry

        # 2. Run test.
        _plot = KoswatLayerPlot()
        _plot.subplot = pyplot.axes()
        _plot.koswat_object = _object
        _axes = _plot.plot("#000")

        # 3. Verify expectations.
        assert _axes is not None

    @pytest.mark.parametrize(
        "geometry",
        [
            pytest.param(Polygon(LineString(_coordinates)), id="Polygon"),
            pytest.param(
                MultiPolygon([Polygon(LineString(_coordinates))]),
                id="MultiPolygon",
            ),
        ],
    )
    def test_when_plot_given_koswat_reinforcement_geometry_then_returns_axes(
        self, geometry: Polygon | MultiPolygon
    ):
        # 1. Define test data.
        assert geometry.is_valid
        _object = ReinforcementCoatingLayer()
        _object.material_type = KoswatMaterialType.SAND
        _object.upper_points = geometry.convex_hull.boundary
        _object.outer_geometry = Polygon(geometry.convex_hull)
        _object.new_layer_surface = geometry.boundary

        # 2. Run test.
        _plot = KoswatLayerPlot()
        _plot.subplot = pyplot.axes()
        _plot.koswat_object = _object
        _axes = _plot.plot("#000")

        # 3. Verify expectations.
        assert _axes is not None
