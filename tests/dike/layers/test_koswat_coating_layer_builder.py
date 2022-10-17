import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_coating_layer_builder import KoswatCoatingLayerBuilder
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol


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
