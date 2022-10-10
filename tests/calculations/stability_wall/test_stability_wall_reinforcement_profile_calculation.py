import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.stability_wall.stability_wall_reinforcement_profile_calculation import (
    StabilityWallReinforcementProfileCalculation,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests import plot_profiles
from tests.calculations import compare_koswat_profiles
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestStabilityWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    @pytest.mark.parametrize(
        "profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_stability_wall_default_scenario_3_no_layers,
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
        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=_dummy_layers,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()
        assert isinstance(_base_profile, KoswatProfileBase)
        _scenario = KoswatScenario.from_dict(dict(scenario_data))
        assert isinstance(_scenario, KoswatScenario)

        # 2. Run test.
        _builder = StabilityWallReinforcementProfileCalculation()
        _builder.base_profile = _base_profile
        _builder.scenario = _scenario
        _new_profile = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_new_profile, PipingWallReinforcementProfile)
        assert isinstance(_new_profile.input_data, KoswatInputProfileBase)
        compare_koswat_profiles(_new_profile, _expected_profile)
        plot_profiles(_base_profile, _new_profile)
