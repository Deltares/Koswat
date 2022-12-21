import math
from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from tests.library_test_cases import InitialPointsLookup, InputProfileCases, LayersCases


class TestKoswatProfileBuilder:
    def test_initialize(self):
        _builder = KoswatProfileBuilder()
        assert isinstance(_builder, KoswatProfileBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.input_profile_data
        assert not _builder.layers_data
        assert math.isnan(_builder.p4_x_coordinate)

    @pytest.mark.parametrize(
        "input_dict",
        [
            pytest.param(
                dict(),
                id="Missing Input Profile Data and Layers",
            ),
            pytest.param(
                dict(input_profile_data=None),
                id="Missing Layers",
            ),
            pytest.param(dict(layers_data=None), id="Missing Input Profile Data"),
        ],
    )
    def test_initialize_with_data_missing_item_raises_error(self, input_dict: dict):
        with pytest.raises(KeyError):
            KoswatProfileBuilder.with_data(input_dict)

    @pytest.mark.parametrize(
        "input_dict",
        [
            pytest.param(
                dict(
                    input_profile_data=InputProfileCases.default,
                    layers_data=LayersCases.without_layers,
                ),
                id="No p4_x coordinate",
            ),
            pytest.param(
                dict(
                    input_profile_data=InputProfileCases.default,
                    layers_data=LayersCases.without_layers,
                    p4_x_coordinate=0,
                ),
                id="Given p4_x coordinate",
            ),
        ],
    )
    def test_initialized_with_data(self, input_dict: dict):
        # 2. Run test.
        _profile_builder = KoswatProfileBuilder.with_data(input_dict)

        # 3. Verify final expectations.
        assert isinstance(_profile_builder, KoswatProfileBuilder)
        assert isinstance(
            _profile_builder.input_profile_data, KoswatInputProfileProtocol
        )
        assert isinstance(_profile_builder.layers_data, dict)
        assert _profile_builder.input_profile_data == input_dict["input_profile_data"]
        assert _profile_builder.layers_data == input_dict["layers_data"]

    def test_build_given_no_input_profile_data_then_raises(self):
        _builder = KoswatProfileBuilder()
        _builder.input_profile_data = None
        _builder.layers_data = dict(base_layer=dict(material="zand"), coating_layers=[])
        _builder.profile_type = None
        with pytest.raises(ValueError) as exc_err:
            _builder.build()
        assert str(exc_err.value) == "Koswat Input Profile data instance required."

    def test_build_given_no_layers_data_then_raises(self):
        _builder = KoswatProfileBuilder()
        _builder.input_profile_data = InputProfileCases.default
        _builder.layers_data = None
        _builder.profile_type = None
        with pytest.raises(ValueError) as exc_err:
            _builder.build()
        assert str(exc_err.value) == "Koswat Layers data dictionary required."

    @pytest.mark.parametrize(
        "input_profile_data, expected_points",
        [
            pytest.param(
                InputProfileCases.default,
                InitialPointsLookup.default,
                id="Initial profile case",
            ),
            pytest.param(
                InputProfileCases.profile_case_2,
                InitialPointsLookup.calc_profile_scenario_2,
                id="Aftermath Default input and default scenario",
            ),
        ],
    )
    def test_given_valid_data_when_build_returns_profile(
        self, input_profile_data: dict, expected_points: List[Point]
    ):
        # 1. Define test data.
        _layers_data = dict(base_layer=dict(material="zand"), coating_layers=[])
        _p4_x_coordinate = expected_points[3].x
        # 2. Run test.
        _profile_builder = KoswatProfileBuilder()
        _profile_builder.profile_type = KoswatProfileBase
        _profile_builder.input_profile_data = input_profile_data
        _profile_builder.layers_data = _layers_data
        _profile_builder.p4_x_coordinate = _p4_x_coordinate
        _koswat_profile = _profile_builder.build()

        # 3. Verify final expectations.
        assert isinstance(_koswat_profile, KoswatProfileBase)
        assert isinstance(_koswat_profile.input_data, KoswatInputProfileBase)
        assert isinstance(_koswat_profile.layers_wrapper, KoswatLayersWrapper)
        for p_idx, p in enumerate(expected_points):
            assert p.almost_equals(_koswat_profile.points[p_idx], 0.001)
