import pytest
from shapely.geometry import LineString, Point, Polygon

from koswat.core.protocols import BuilderProtocol
from koswat.dike.layers import KoswatLayerBuilderProtocol, KoswatLayerProtocol
from koswat.dike.layers.coating_layer import (
    KoswatCoatingLayer,
    KoswatCoatingLayerBuilder,
)


class TestKoswatCoatingLayerBuilder:
    def test_initialize(self):
        _builder = KoswatCoatingLayerBuilder()
        assert isinstance(_builder, KoswatCoatingLayerBuilder)
        assert isinstance(_builder, KoswatLayerBuilderProtocol)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.upper_linestring
        assert not _builder.layer_data
        assert not _builder.base_geometry

    @pytest.mark.parametrize(
        "upper_linestring, layer_data, base_geometry",
        [
            pytest.param(None, None, None, id="No args given"),
            pytest.param("sth", None, None, id="Only upper_linestring"),
            pytest.param(None, "sth", None, id="Only layer_data"),
            pytest.param(None, None, "sth", id="Only base_geometry"),
            pytest.param("sth", "sth", None, id="Missing base_geometry"),
            pytest.param("sth", None, "sth", id="Missing layer_data"),
            pytest.param(None, "sth", "sth", id="Missing upper_linestring"),
        ],
    )
    def test_when_build_given_missing_args_then_raises(
        self, upper_linestring, layer_data, base_geometry
    ):
        # 1. Define test data.
        _expected_err = "All coating layer builder fields are required."
        _builder = KoswatCoatingLayerBuilder()
        _builder.upper_linestring = upper_linestring
        _builder.layer_data = layer_data
        _builder.base_geometry = base_geometry

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _builder.build()

        # 3. Verify expectations.
        assert str(exc_err.value) == _expected_err

    def test_given_valid_data_when_build_then_returns_koswat_coating_layer(self):
        # 1. Define test data
        _builder = KoswatCoatingLayerBuilder()
        _points = list(map(Point, [(0, 0), (3, 3), (4, 5), (5, 3), (8, 0)]))
        _builder.upper_linestring = LineString(_points)
        _builder.layer_data = dict(material="klei", depth=1)
        _points.append(_points[0])
        _builder.base_geometry = Polygon(_points)

        # 2. Run test
        _coating_layer = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_coating_layer, KoswatCoatingLayer)
        assert isinstance(_coating_layer, KoswatLayerProtocol)

    def test_get_offset_geometry(self):
        # 1. Define test data
        _builder = KoswatCoatingLayerBuilder()
        _points = [(0, 0), (3, 3), (4, 5), (5, 3), (8, 0)]

        # 2. Run test
        _offset_geometry = _builder._get_offset_geometry(list(map(Point, _points)))

        # 3. Verify expectations.
        for idx, coord in enumerate(_offset_geometry.coords):
            pos = len(_points) - (idx + 1)
            assert coord == _points[pos]
