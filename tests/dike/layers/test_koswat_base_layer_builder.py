import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_base_layer_builder import KoswatBaseLayerBuilder
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol


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
