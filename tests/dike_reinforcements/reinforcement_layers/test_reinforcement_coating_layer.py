import pytest
from shapely.geometry import LineString, Polygon

from koswat.dike.layers.coating_layer.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementCoatingLayer,
)


class TestReinforcementCoatingLayer:
    @pytest.fixture
    def dummy_coating_layer(self) -> KoswatCoatingLayer:
        _test_coating_layer = KoswatCoatingLayer()
        _test_coating_layer.depth = 4.2
        _test_coating_layer.lower_linestring = LineString([(0, 0), (0, 4)])
        _test_coating_layer.upper_points = LineString([(4, 0), (4, 4)])
        _test_coating_layer.material_type = KoswatMaterialType.CLAY
        _test_coating_layer.outer_geometry = Polygon(
            [(0, 0), (3, 3), (4, 5), (5, 3), (8, 0)]
        )
        _test_coating_layer.material_geometry = Polygon(
            [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        )
        yield _test_coating_layer

    def test_from_coating_layer_returns_expected_layer(
        self, dummy_coating_layer: KoswatCoatingLayer
    ):
        # 1. Define test data.
        assert isinstance(dummy_coating_layer, KoswatCoatingLayer)

        # 2. Run test.
        _result = ReinforcementCoatingLayer.from_koswat_coating_layer(
            dummy_coating_layer
        )

        # 3. Verify expectations.
        assert isinstance(_result, ReinforcementCoatingLayer)
        assert _result.depth == dummy_coating_layer.depth
        assert _result.lower_linestring == dummy_coating_layer.lower_linestring
        assert _result.upper_points == dummy_coating_layer.upper_points
        assert _result.material_type == dummy_coating_layer.material_type
        assert _result.outer_geometry == dummy_coating_layer.outer_geometry
        assert _result.material_geometry == dummy_coating_layer.material_geometry

    def test_with_same_outer_geometry_returns_expected_layer(
        self, dummy_coating_layer: KoswatCoatingLayer
    ):
        # 1. Define test data.
        assert isinstance(dummy_coating_layer, KoswatCoatingLayer)
        assert not dummy_coating_layer.outer_geometry.is_empty

        # 2. Run test.
        _result = ReinforcementCoatingLayer.with_same_outer_geometry(
            dummy_coating_layer
        )

        # 3. Verify expectations.
        assert isinstance(_result, ReinforcementCoatingLayer)
        assert _result.old_layer_geometry == dummy_coating_layer.outer_geometry

        assert isinstance(_result.removal_layer_geometry, Polygon)
        assert _result.removal_layer_geometry.is_empty

        assert isinstance(_result.new_layer_geometry, Polygon)
        assert _result.new_layer_geometry.is_empty

        assert isinstance(_result.new_layer_surface, LineString)
        assert _result.new_layer_surface.is_empty
