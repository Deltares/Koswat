import pytest

from koswat.profiles.koswat_layers import KoswatLayer, KoswatLayers
from koswat.profiles.koswat_layers_builder import KoswatLayersBuilder
from tests.library_test_cases import InputProfileCases, LayersCases


class TestKoswatLayersBuilder:
    def test_initialize(self):
        _builder = KoswatLayersBuilder()
        assert isinstance(_builder, KoswatLayersBuilder)
        assert not _builder.layers_data
        assert not _builder.profile_points

    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    def test_build_given_valid_data(self, layers_case: dict):
        # 1. Define test data.
        _layers_builder = KoswatLayersBuilder()
        _layers_builder.layers_data = layers_case
        _layers_builder.profile_points = InputProfileCases.default_points
        # 2. Run test
        _layers = _layers_builder.build()

        # 3. Verify expectations
        assert isinstance(_layers, KoswatLayers)
        assert isinstance(_layers.base_layer, KoswatLayer)
        assert isinstance(_layers.coating_layers, list)
        assert len(_layers.coating_layers) == len(layers_case["coating_layers"])
        for c_layer in _layers.coating_layers:
            assert isinstance(c_layer, KoswatLayer)
