import shutil
from typing import Type

import pytest

from koswat.calculations import (
    CofferdamReinforcementProfile,
    CofferdamReinforcementProfileCalculation,
    PipingWallReinforcementProfile,
    PipingWallReinforcementProfileCalculation,
    ReinforcementProfileCalculationProtocol,
    ReinforcementProfileProtocol,
    SoilReinforcementProfile,
    SoilReinforcementProfileCalculation,
    StabilityWallReinforcementProfile,
    StabilityWallReinforcementProfileCalculation,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests import get_fixturerequest_case_name, plot_profiles, test_results
from tests.calculations import compare_koswat_profiles
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestReinforcementProfileCalculationProtocol:
    def test_initialize(self):
        with pytest.raises(TypeError):
            ReinforcementProfileCalculationProtocol()

    @pytest.mark.parametrize(
        "profile_type, calculation_type, profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                PipingWallReinforcementProfile,
                PipingWallReinforcementProfileCalculation,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_piping_wall_default_scenario_3_no_layers,
                id="Piping Wall, Default input profile, Scenario 3",
            ),
            pytest.param(
                StabilityWallReinforcementProfile,
                StabilityWallReinforcementProfileCalculation,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_stability_wall_default_scenario_3_no_layers,
                id="Stability Wall, Default input profile, Scenario 3",
            ),
            pytest.param(
                SoilReinforcementProfile,
                SoilReinforcementProfileCalculation,
                InputProfileCases.default,
                ScenarioCases.default,
                InputProfileScenarioLookup.reinforcement_soil_default_default_no_layers,
                id="Soil, Default input profile, Default Scenario",
            ),
            pytest.param(
                SoilReinforcementProfile,
                SoilReinforcementProfileCalculation,
                InputProfileCases.default,
                ScenarioCases.scenario_2,
                InputProfileScenarioLookup.reinforcement_soil_default_scenario_2_no_layers,
                id="Soil, Default input profile, Scenario 2",
            ),
            pytest.param(
                CofferdamReinforcementProfile,
                CofferdamReinforcementProfileCalculation,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_coffer_dam_wall_default_scenario_3_no_layers,
            ),
        ],
    )
    def test_given_profile_and_scenario_calculate_new_geometry(
        self,
        profile_type: Type[ReinforcementProfileProtocol],
        calculation_type: Type[ReinforcementProfileCalculationProtocol],
        profile_data: dict,
        scenario_data: dict,
        expected_profile_data: dict,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _plot_dir = test_results / get_fixturerequest_case_name(request)
        if _plot_dir.is_dir():
            shutil.rmtree(_plot_dir)
        _plot_dir.mkdir(parents=True)

        _dummy_layers = LayersCases.without_layers
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
        _builder = calculation_type()
        _builder.base_profile = _base_profile
        _builder.scenario = _scenario
        _new_profile = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_new_profile, profile_type)
        assert isinstance(_new_profile, KoswatProfileProtocol)
        assert isinstance(_new_profile.input_data, KoswatInputProfileBase)
        assert isinstance(_new_profile.input_data, KoswatInputProfileProtocol)
        _plot = plot_profiles(_base_profile, _new_profile)
        _plot_filename = _plot_dir / str(_new_profile)
        _plot_filename.with_suffix(".png")
        _plot.savefig(_plot_filename)

        expected_profile_data["profile_type"] = profile_type
        _expected_profile = KoswatProfileBuilder.with_data(
            expected_profile_data
        ).build()
        assert isinstance(_expected_profile, profile_type)
        compare_koswat_profiles(_new_profile, _expected_profile)
