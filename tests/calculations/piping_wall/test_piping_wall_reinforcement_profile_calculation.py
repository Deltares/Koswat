from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile_calculation import (
    PipingWallReinforcementProfileCalculation,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.koswat_layers import KoswatLayers
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests.calculations import compare_koswat_profiles
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestPipingWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = PipingWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, PipingWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_length_stability_wall(self):
        class MockProfile(KoswatInputProfileProtocol):
            binnen_berm_breedte: float

        # 1. Define test data.
        _calculator = PipingWallReinforcementProfileCalculation()
        _profile_data = MockProfile()
        _profile_data.binnen_berm_breedte = 6
        _expected_result = 2.5

        # 2. Run test.
        _result = _calculator._calculate_length_stability_wall(_profile_data)

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_length_stability_wall(self):
        class MockProfile(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = PipingWallReinforcementProfileCalculation()
        _profile_data = MockProfile()
        _profile_data.kruin_hoogte = 4.2
        _scenario = KoswatScenario()
        _scenario.d_h = 2.4
        _expected_result = 6.6

        # 2. Run test.
        _result = _calculator._calculate_new_kruin_hoogte(_profile_data)

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_new_binnen_talud(self):
        class MockProfile(KoswatInputProfileProtocol):
            kruin_hoogte: float
            kruin_breedte: float
            binnen_talud: float

        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = MockProfile()
        _input_profile.kruin_breedte = 5
        _input_profile.kruin_hoogte = 6
        _input_profile.binnen_talud = 3

        # 2. Run test
        _new_binnen_talud = (
            PipingWallReinforcementProfileCalculation()._calculate_new_binnen_talud(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)

    @pytest.mark.parametrize(
        "profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_piping_wall_default_scenario_3_no_layers,
                id="Default input profile, Scenario 3",
            ),
        ],
    )
    def test_given_profile_and_scenario_calculate_new_geometry(
        self,
        profile_data: dict,
        scenario_data: dict,
        expected_profile_data: dict,
    ):
        # 1. Define test data.
        _dummy_layers = LayersCases.without_layers
        expected_profile_data["profile_type"] = PipingWallReinforcementProfile
        _expected_profile = KoswatProfileBuilder.with_data(
            expected_profile_data
        ).build()
        assert isinstance(_expected_profile, PipingWallReinforcementProfile)
        _profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=_dummy_layers,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()
        assert isinstance(_profile, KoswatProfileBase)
        _scenario = KoswatScenario.from_dict(dict(scenario_data))
        assert isinstance(_scenario, KoswatScenario)

        # 2. Run test.
        _builder = PipingWallReinforcementProfileCalculation()
        _builder.base_profile = _profile
        _builder.scenario = _scenario
        _new_profile = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_new_profile, PipingWallReinforcementProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfileBase)
        compare_koswat_profiles(_new_profile, _expected_profile)
