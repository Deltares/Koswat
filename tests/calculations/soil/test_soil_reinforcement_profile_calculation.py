import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.soil.soil_reinforcement_profile import SoilReinforcementProfile
from koswat.calculations.soil.soil_reinforcement_profile_calculation import (
    SoilReinforcementProfileCalculation,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests.calculations import compare_koswat_profiles
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestSoilReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = SoilReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, SoilReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    @pytest.mark.parametrize(
        "profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.default,
                InputProfileScenarioLookup.reinforcement_soil_default_default_no_layers,
                id="Default input profile, Default Scenario",
            ),
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.scenario_2,
                InputProfileScenarioLookup.reinforcement_soil_default_scenario_2_no_layers,
                id="Default input profile, Scenario 2",
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
        expected_profile_data["profile_type"] = SoilReinforcementProfile
        _expected_profile = KoswatProfileBuilder.with_data(
            expected_profile_data
        ).build()
        assert isinstance(_expected_profile, SoilReinforcementProfile)
        _profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=_dummy_layers,
                p4_x_coordinate=0,
                profile_type=SoilReinforcementProfile,
            )
        ).build()
        assert isinstance(_profile, SoilReinforcementProfile)
        _scenario = KoswatScenario.from_dict(dict(scenario_data))
        assert isinstance(_scenario, KoswatScenario)

        # 2. Run test.
        _builder = SoilReinforcementProfileCalculation()
        _builder.base_profile = _profile
        _builder.scenario = _scenario
        _new_profile = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_new_profile, SoilReinforcementProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfileBase)
        compare_koswat_profiles(_new_profile, _expected_profile)

    def test_calculate_new_binnen_talud(self):
        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = KoswatInputProfileBase()
        _input_profile.kruin_breedte = 5
        _input_profile.kruin_hoogte = 6
        _input_profile.binnen_talud = 3

        # 2. Run test
        _new_binnen_talud = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_talud(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte(self):
        # 1. Define test data.
        _expected_value = 1
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _old_data = KoswatInputProfileBase()
        _old_data.binnen_berm_hoogte = 0
        _old_data.kruin_hoogte = 6
        _new_data = KoswatInputProfileBase()
        _new_data.binnen_berm_breedte = 20

        # 2. Run test
        _new_binnen_berm_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte_negative_binnen_berm_breedte(self):
        # 1. Define test data.
        _expected_value = 0
        _scenario = KoswatScenario()
        _old_data = KoswatInputProfileBase()
        _new_data = KoswatInputProfileBase()
        _new_data.binnen_berm_breedte = -1

        # 2. Run test
        _new_binnen_berm_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_breedte(self):
        # 1. Define test data.
        _expected_value = 20
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_p = 30
        _scenario.buiten_talud = 3
        _old_profile = KoswatInputProfileBase()
        _old_profile.buiten_maaiveld = 0
        _old_profile.buiten_talud = 3
        _old_profile.buiten_berm_hoogte = 0
        _old_profile.buiten_berm_breedte = 0
        _old_profile.kruin_hoogte = 6
        _old_profile.kruin_breedte = 5
        _old_profile.binnen_talud = 3
        _old_profile.binnen_berm_hoogte = 0
        _old_profile.binnen_berm_breedte = 0
        _old_profile.binnen_maaiveld = 0
        _new_profile = KoswatInputProfileBase()
        _new_profile.binnen_talud = 3.5714
        _new_profile.buiten_berm_breedte = 0
        _new_profile.kruin_breedte = 5

        # 2. Run test
        _new_binnen_berm_breedte = (
            SoilReinforcementProfileCalculation()._calculate_new_binnen_berm_breedte(
                _old_profile, _new_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_breedte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_kruin_hoogte(self):
        # 1. Define test data.
        _expected_value = 42.24
        _scenario = KoswatScenario()
        _scenario.d_h = 2.2
        _old_data = KoswatInputProfileBase()
        _old_data.kruin_hoogte = 40.04

        # 2. Run test
        _new_kruin_hoogte = (
            SoilReinforcementProfileCalculation()._calculate_new_kruin_hoogte(
                _old_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_kruin_hoogte == pytest.approx(_expected_value, 0.001)
