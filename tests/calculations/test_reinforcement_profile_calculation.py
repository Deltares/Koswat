from pathlib import Path
from typing import Type

import pytest

from koswat.calculations import (
    ReinforcementInputProfileCalculationProtocol,
    ReinforcementInputProfileProtocol,
    ReinforcementProfileBuilderFactory,
    ReinforcementProfileBuilderProtocol,
    ReinforcementProfileProtocol,
)
from koswat.calculations.outside_slope_reinforcement import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.standard_reinforcement import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from koswat.plots import get_plot
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from tests import get_testcase_results_dir
from tests.calculations import get_reinforced_profile, validated_reinforced_profile
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestReinforcementProfileCalculationProtocol:
    def test_initialize(self):
        with pytest.raises(TypeError):
            ReinforcementInputProfileCalculationProtocol()


class TestReinforcementProfileBuilderFactory:
    def test_get_available_reinforcements(self):
        _expected_reinforcements = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]
        _available_reinforcements = (
            ReinforcementProfileBuilderFactory.get_available_reinforcements()
        )
        assert len(_available_reinforcements) == 4
        assert all(
            _reinforcement in _available_reinforcements
            for _reinforcement in _expected_reinforcements
        )

    @pytest.mark.parametrize(
        "reinforcement_profile_type, expected_builder",
        [
            pytest.param(
                SoilReinforcementProfile,
                StandardReinforcementProfileBuilder,
                id="[Standard] Soil reinforcement",
            ),
            pytest.param(
                PipingWallReinforcementProfile,
                StandardReinforcementProfileBuilder,
                id="[Standard] Piping wall reinforcement",
            ),
            pytest.param(
                StabilityWallReinforcementProfile,
                StandardReinforcementProfileBuilder,
                id="[Standard] Stability wall reinforcement",
            ),
            pytest.param(
                CofferdamReinforcementProfile,
                OutsideSlopeReinforcementProfileBuilder,
                id="[Oustide Slope] Cofferdam reinforcement",
            ),
        ],
    )
    def test_get_builder(
        self,
        reinforcement_profile_type: Type[ReinforcementProfileProtocol],
        expected_builder: ReinforcementProfileBuilderProtocol,
    ):
        _builder = ReinforcementProfileBuilderFactory.get_builder(
            reinforcement_profile_type
        )
        # Verify expectations.
        assert _builder.reinforcement_profile_type == reinforcement_profile_type
        assert isinstance(_builder, expected_builder)
        assert isinstance(_builder, ReinforcementProfileBuilderProtocol)

    @pytest.mark.parametrize(
        "profile_type, profile_data, scenario_data, expected_profile_data",
        [
            pytest.param(
                PipingWallReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_piping_wall_default_scenario_3_no_layers,
                id="Piping Wall, Default input profile, Scenario 3",
            ),
            pytest.param(
                StabilityWallReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_stability_wall_default_scenario_3_no_layers,
                id="Stability Wall, Default input profile, Scenario 3",
            ),
            pytest.param(
                SoilReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.default,
                InputProfileScenarioLookup.reinforcement_soil_default_default_no_layers,
                id="Soil, Default input profile, Default Scenario",
            ),
            pytest.param(
                SoilReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.scenario_2,
                InputProfileScenarioLookup.reinforcement_soil_default_scenario_2_no_layers,
                id="Soil, Default input profile, Scenario 2",
            ),
            pytest.param(
                CofferdamReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_coffer_dam_wall_default_scenario_3_no_layers,
            ),
        ],
    )
    def test_given_profile_and_scenario_calculate_new_geometry(
        self,
        profile_type: Type[ReinforcementProfileProtocol],
        profile_data: dict,
        scenario_data: dict,
        expected_profile_data: dict,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _plot_dir = get_testcase_results_dir(request)
        _dummy_layers = LayersCases.without_layers
        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=_dummy_layers,
                p4_x_coordinate=0,
            )
        ).build()
        _scenario = KoswatScenario.from_dict(dict(scenario_data))
        _expected_profile = get_reinforced_profile(profile_type, expected_profile_data)
        assert isinstance(_base_profile, KoswatProfileBase)
        assert isinstance(_expected_profile, profile_type)
        assert isinstance(_expected_profile, ReinforcementProfileProtocol)
        assert isinstance(_scenario, KoswatScenario)

        # 2. Run test.
        _reinforcement_builder = ReinforcementProfileBuilderFactory.get_builder(
            profile_type
        )
        _reinforcement_builder.base_profile = _base_profile
        _reinforcement_builder.scenario = _scenario
        _reinforcement_profile = _reinforcement_builder.build()

        # 3. Verify expectations.
        assert isinstance(_reinforcement_profile, profile_type)
        assert isinstance(_reinforcement_profile, ReinforcementProfileProtocol)
        assert isinstance(_reinforcement_profile, KoswatProfileProtocol)
        assert isinstance(
            _reinforcement_profile.input_data, ReinforcementInputProfileProtocol
        )
        validated_reinforced_profile(_reinforcement_profile, _expected_profile)
        self._plot_profiles(_base_profile, _reinforcement_profile)

    def _plot_profiles(
        self,
        base_profile: KoswatProfileProtocol,
        reinforced_profile: ReinforcementProfileProtocol,
        output_dir: Path,
    ):
        _figure = get_plot(180)
        _subplot = _figure.add_subplot()
        _list_profile_plot = ListKoswatProfilePlot()
        _list_profile_plot.koswat_object = [
            (base_profile, "#03a9fc"),
            (reinforced_profile, "#fc0303"),
        ]
        _list_profile_plot.subplot = _subplot
        _list_profile_plot.plot()
        # Export
        _plot_filename = output_dir / str(reinforced_profile)
        _figure.savefig(_plot_filename.with_suffix(".png"))
