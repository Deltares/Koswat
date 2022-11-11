import pytest
from shapely.geometry import LineString

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer, KoswatBaseLayerBuilder
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


class TestKoswatBaseLayerBuilder:
    def test_initialize(self):
        _builder = KoswatBaseLayerBuilder()
        assert isinstance(_builder, KoswatBaseLayerBuilder)
        assert isinstance(_builder, KoswatLayerBuilderProtocol)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.upper_linestring
        assert not _builder.layer_data

    def test_build_raises_when_no_upper_linestring_given(self):
        _builder = KoswatBaseLayerBuilder()
        with pytest.raises(ValueError) as exc_err:
            _builder.build()
        assert str(exc_err.value) == "Profile line geometry needs to be provided."

    def test_build_raises_when_no_material_data_given(self):
        _builder = KoswatBaseLayerBuilder()
        _builder.upper_linestring = "something"
        with pytest.raises(ValueError) as exc_err:
            _builder.build()
        assert str(exc_err.value) == "Material data needs to be provided."

    def test_when_build_given_valid_data_returns_koswat_base_layer(self):
        # 1. Define test data
        _builder = KoswatBaseLayerBuilder()
        _builder.layer_data = dict(material="zand")
        x_coords = range(0, 5)
        y_coords = [0, 2, 4, 2, 0]
        _builder.upper_linestring = LineString(zip(x_coords, y_coords))

        # 2. Run test
        _base_layer = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_base_layer, KoswatBaseLayer)
        assert isinstance(_base_layer, KoswatLayerProtocol)
