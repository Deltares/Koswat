from typing import List

import pytest
from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.profiles.koswat_layers import (
    KoswatBaseLayer,
    KoswatCoatingLayer,
    KoswatLayers,
)
from koswat.profiles.koswat_layers_builder import KoswatLayersBuilder
from koswat.profiles.koswat_material import KoswatMaterial
from tests.library_test_cases import InitialPointsLookup, InputProfileCases, LayersCases


class TestKoswatLayersBuilder:
    def test_initialize(self):
        _builder = KoswatLayersBuilder()
        assert isinstance(_builder, KoswatLayersBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.layers_data
        assert not _builder.profile_points

    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    @pytest.mark.parametrize("profile_points", InitialPointsLookup.cases)
    def test_build_given_valid_data(
        self, layers_case: dict, profile_points: List[Point]
    ):
        # 1. Define test data.
        _layers_builder = KoswatLayersBuilder()
        _layers_builder.layers_data = layers_case
        _layers_builder.profile_points = profile_points
        # 2. Run test
        _layers = _layers_builder.build()

        # 3. Verify expectations
        assert isinstance(_layers, KoswatLayers)
        assert isinstance(_layers.base_layer, KoswatBaseLayer)
        assert isinstance(_layers.base_layer.material, KoswatMaterial)
        assert _layers.base_layer.material.name == layers_case["base_layer"]["material"]
        assert len(_layers.coating_layers) == len(layers_case["coating_layers"])
        for c_idx, c_layer in enumerate(_layers.coating_layers):
            assert isinstance(c_layer, KoswatCoatingLayer)
            assert c_layer.depth == layers_case["coating_layers"][c_idx]["depth"]
            assert isinstance(c_layer.material, KoswatMaterial)
            assert (
                c_layer.material.name
                == layers_case["coating_layers"][c_idx]["material"]
            )
