from typing import List

import pytest
from shapely.geometry import Point

from koswat.core.protocols import BuilderProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.layers.layers_wrapper import (
    KoswatLayersWrapper,
    KoswatLayersWrapperBuilder,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from tests.acceptance_scenarios.initial_characteristic_points_cases import (
    InitialPointsLookup,
)
from tests.acceptance_scenarios.layers_cases import LayersCases


class TestKoswatLayersWrapperBuilder:
    def test_initialize(self):
        _builder = KoswatLayersWrapperBuilder()
        assert isinstance(_builder, KoswatLayersWrapperBuilder)
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
        _layers_builder = KoswatLayersWrapperBuilder()
        _layers_builder.layers_data = layers_case
        _layers_builder.profile_points = profile_points
        # 2. Run test
        _layers = _layers_builder.build()

        # 3. Verify expectations
        assert isinstance(_layers, KoswatLayersWrapper)
        assert isinstance(_layers.base_layer, KoswatBaseLayer)
        assert isinstance(_layers.base_layer.material_type, KoswatMaterialType)
        assert _layers.base_layer.material_type == layers_case["base_layer"]["material"]
        assert len(_layers.coating_layers) == len(layers_case["coating_layers"])
        for c_idx, c_layer in enumerate(_layers.coating_layers):
            assert isinstance(c_layer, KoswatCoatingLayer)
            assert c_layer.depth == layers_case["coating_layers"][c_idx]["depth"]
            assert isinstance(c_layer.material_type, KoswatMaterialType)
            assert (
                c_layer.material_type
                == layers_case["coating_layers"][c_idx]["material"]
            )
