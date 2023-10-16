from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, List, Type

import pytest

from koswat.calculations import ReinforcementProfileBuilderFactory
from koswat.calculations.outside_slope_reinforcement import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.protocols import (
    ReinforcementInputProfileCalculationProtocol,
    ReinforcementInputProfileProtocol,
    ReinforcementProfileBuilderProtocol,
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)
from koswat.configuration.io.ini.koswat_scenario_list_ini_dir_reader import (
    KoswatSectionScenarioListIniDirReader,
)
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.io.koswat_input_profile_list_importer import (
    KoswatInputProfileListImporter,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from tests import get_custom_testcase_results_dir, get_testcase_results_dir, test_data
from tests.calculations import get_reinforced_profile, validated_reinforced_profile
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


def scenario_ini_file() -> List[pytest.param]:
    scenarios_dir = test_data / "acceptance" / "scenarios"

    def _to_koswat_scenario(
        scenario_data: KoswatSectionScenariosIniFom,
    ) -> Iterable[KoswatScenario]:
        for _section_scenario in scenario_data.section_scenarios:
            _scenario = KoswatScenario()
            _scenario.scenario_section = scenario_data.scenario_dike_section
            _scenario.scenario_name = _section_scenario.scenario_name
            _scenario.d_h = _section_scenario.d_h
            _scenario.d_s = _section_scenario.d_s
            _scenario.d_p = _section_scenario.d_p
            _scenario.kruin_breedte = _section_scenario.kruin_breedte
            _scenario.buiten_talud = _section_scenario.buiten_talud
            yield _scenario

    def _to_pytest_param(scenario: KoswatScenario) -> pytest.param:
        return pytest.param(
            scenario,
            id="{}_{}".format(scenario.scenario_name, scenario.scenario_section),
        )

    _scenarios = []
    for _fom_scenario_wrapper in KoswatSectionScenarioListIniDirReader().read(
        scenarios_dir
    ):
        _scenarios = _scenarios + list(_to_koswat_scenario(_fom_scenario_wrapper))

    return list(map(_to_pytest_param, _scenarios))


def input_profile_data_csv_file() -> List[pytest.param]:
    _csv_file = test_data / "acceptance" / "csv" / "dike_input_profiles.csv"

    def _to_pytest_param(input_profile: KoswatInputProfileBase) -> pytest.param:
        return pytest.param(
            input_profile, id="Input_{}".format(input_profile.dike_section)
        )

    return list(
        map(_to_pytest_param, KoswatInputProfileListImporter().import_from(_csv_file))
    )[:2]


_scenarios = scenario_ini_file()
_input_profiles = input_profile_data_csv_file()


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

    def test_get_reinforcement_input_profile_unknown_reinforcement(self):
        with pytest.raises(NotImplementedError):
            ReinforcementProfileBuilderFactory.get_reinforcement_input_profile(None)

    @pytest.mark.parametrize(
        "reinforcement_profile_type, expected_input_profile_type",
        [
            pytest.param(
                SoilReinforcementProfile,
                SoilInputProfile,
                id="[Standard] Soil reinforcement",
            ),
            pytest.param(
                PipingWallReinforcementProfile,
                PipingWallInputProfile,
                id="[Standard] Piping wall reinforcement",
            ),
            pytest.param(
                StabilityWallReinforcementProfile,
                StabilityWallInputProfile,
                id="[Standard] Stability wall reinforcement",
            ),
            pytest.param(
                CofferdamReinforcementProfile,
                CofferDamInputProfile,
                id="[Oustide Slope] Cofferdam reinforcement",
            ),
        ],
    )
    def test_get_reinforcement_input_profile(
        self,
        reinforcement_profile_type: Type[ReinforcementProfileProtocol],
        expected_input_profile_type,
    ):
        _input_profile = (
            ReinforcementProfileBuilderFactory.get_reinforcement_input_profile(
                reinforcement_profile_type
            )
        )
        assert _input_profile == expected_input_profile_type

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
                CofferdamReinforcementProfile,
                InputProfileCases.default,
                ScenarioCases.scenario_3,
                InputProfileScenarioLookup.reinforcement_coffer_dam_wall_default_scenario_3_no_layers,
            ),
        ],
    )
    def test_given_profile_and_scenario_calculate_new_geometry_without_layers(
        self,
        profile_type: Type[ReinforcementProfileProtocol],
        profile_data: KoswatInputProfileProtocol,
        scenario_data: KoswatScenario,
        expected_profile_data: dict,
        request: pytest.FixtureRequest,
    ):
        # TO-DO, potentially remove as the test below covers better this test case.
        # 1. Define test data.
        _plot_dir = get_testcase_results_dir(request)
        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=profile_data,
                layers_data=LayersCases.without_layers.layers_dict,
                p4_x_coordinate=0,
            )
        ).build()
        _expected_profile = get_reinforced_profile(profile_type, expected_profile_data)
        assert isinstance(_base_profile, KoswatProfileBase)
        assert isinstance(_expected_profile, profile_type)
        assert isinstance(_expected_profile, ReinforcementProfileProtocol)
        assert isinstance(scenario_data, KoswatScenario)

        # 2. Run test.
        _reinforcement_builder = ReinforcementProfileBuilderFactory.get_builder(
            profile_type
        )
        _reinforcement_builder.base_profile = _base_profile
        _reinforcement_builder.scenario = scenario_data
        _reinforcement_profile = _reinforcement_builder.build()

        # 3. Verify expectations.
        assert isinstance(_reinforcement_profile, profile_type)
        assert isinstance(_reinforcement_profile, ReinforcementProfileProtocol)
        assert isinstance(_reinforcement_profile, KoswatProfileProtocol)
        assert isinstance(
            _reinforcement_profile.input_data, ReinforcementInputProfileProtocol
        )
        validated_reinforced_profile(_reinforcement_profile, _expected_profile)
        self._plot_profiles(_base_profile, _reinforcement_profile, _plot_dir)

    @pytest.mark.parametrize(
        "profile_type",
        [
            pytest.param(SoilReinforcementProfile, id="Groundmaatregel"),
            pytest.param(PipingWallReinforcementProfile, id="Pipingwand"),
            pytest.param(StabilityWallReinforcementProfile, id="Stabiliteitswand"),
            pytest.param(CofferdamReinforcementProfile, id="Kistdam"),
        ],
    )
    @pytest.mark.parametrize("input_profile", _input_profiles)
    @pytest.mark.parametrize("scenario", _scenarios)
    def test_generate_reinforcement_profiles_from_acceptance_data(
        self,
        profile_type: Type[ReinforcementProfileProtocol],
        input_profile: KoswatInputProfileProtocol,
        scenario: KoswatScenario,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _plot_dir = get_custom_testcase_results_dir(request, -1)
        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=input_profile,
                layers_data=LayersCases.with_acceptance_criteria.layers_dict,
                p4_x_coordinate=0,
            )
        ).build()
        assert isinstance(_base_profile, KoswatProfileBase)

        # Correct scenario.
        if not scenario.buiten_talud or math.isnan(scenario.buiten_talud):
            scenario.buiten_talud = input_profile.buiten_talud
        if not scenario.kruin_breedte or math.isnan(scenario.kruin_breedte):
            scenario.kruin_breedte = input_profile.kruin_breedte

        # 2. Run test.
        _reinforcement_builder = ReinforcementProfileBuilderFactory.get_builder(
            profile_type
        )
        _reinforcement_builder.base_profile = _base_profile
        _reinforcement_builder.scenario = scenario
        _reinforcement_profile = _reinforcement_builder.build()

        # 3. Verify expectations.
        assert isinstance(_reinforcement_profile, profile_type)
        assert isinstance(_reinforcement_profile, ReinforcementProfileProtocol)
        assert isinstance(_reinforcement_profile, KoswatProfileProtocol)
        assert isinstance(
            _reinforcement_profile.input_data, ReinforcementInputProfileProtocol
        )
        self._plot_profiles(_base_profile, _reinforcement_profile, _plot_dir)

    def _plot_profiles(
        self,
        base_profile: KoswatProfileProtocol,
        reinforced_profile: ReinforcementProfileProtocol,
        output_dir: Path,
    ):
        _plot_filename = output_dir / str(reinforced_profile)
        with KoswatFigureContextHandler(
            _plot_filename.with_suffix(".png"), 250
        ) as _koswat_figure:
            _subplot = _koswat_figure.add_subplot()
            _list_profile_plot = ListKoswatProfilePlot()
            _list_profile_plot.koswat_object = [
                (base_profile, "#03a9fc"),
                (reinforced_profile, "#fc0303"),
            ]
            _list_profile_plot.subplot = _subplot
            _list_profile_plot.plot()
