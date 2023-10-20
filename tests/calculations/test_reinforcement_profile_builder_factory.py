from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import pytest

from koswat.dike_reinforcements import ReinforcementProfileBuilderFactory
from koswat.dike_reinforcements.reinforcement_profile.outside_slope_reinforcement_profiles import (
    CofferdamReinforcementProfile,
)

from koswat.dike_reinforcements.reinforcement_layers.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope_reinforcement_profiles.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.input_profile import (
    PipingWallInputProfile,
    SoilInputProfile,
    StabilityWallInputProfile,
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope_reinforcement_profiles.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.standard_reinforcement_profiles.standard_reinforcement_profile_builder import (
    StandardReinforcementProfile,
    StandardReinforcementProfileBuilder,
)
from koswat.dike_reinforcements.reinforcement_layers.standard_reinforcement_layers_wrapper_builder import (
    StandardReinforcementLayersWrapperBuilder,
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
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder import (
    KoswatLayersWrapperBuilder,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder_protocol import (
    KoswatLayersWrapperBuilderProtocol,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_protocol import (
    KoswatLayersWrapperProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from tests import get_custom_testcase_results_dir, get_testcase_results_dir, test_data
from tests.acceptance_scenarios.layers_cases import LayersCases
from tests.calculations import validated_reinforced_profile
from tests.calculations.reinforcement_profile_cases import (
    ReinforcementProfileCase,
    ReinforcementProfileCaseCombination,
    reinforcement_profile_cases,
)


def scenario_ini_file() -> list[pytest.param]:
    scenarios_dir = test_data / "acceptance" / "scenarios"

    def _to_koswat_scenario(
        scenario_data: KoswatSectionScenariosIniFom,
    ) -> Iterable[KoswatScenario]:
        for _section_scenario in scenario_data.section_scenarios:
            _scenario = KoswatScenario(
                d_h=_section_scenario.d_h,
                d_s=_section_scenario.d_s,
                d_p=_section_scenario.d_p,
                scenario_section=scenario_data.scenario_dike_section,
                scenario_name=_section_scenario.scenario_name,
                kruin_breedte=_section_scenario.kruin_breedte,
                buiten_talud=_section_scenario.buiten_talud,
            )
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


def input_profile_data_csv_file() -> list[pytest.param]:
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
        reinforcement_profile_type: type[ReinforcementProfileProtocol],
        expected_input_profile_type: type[SoilInputProfile]
        | type[PipingWallInputProfile]
        | type[StabilityWallInputProfile]
        | type[CofferDamInputProfile],
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
        reinforcement_profile_type: type[ReinforcementProfileProtocol],
        expected_builder: ReinforcementProfileBuilderProtocol,
    ):
        _builder = ReinforcementProfileBuilderFactory.get_builder(
            reinforcement_profile_type
        )
        # Verify expectations.
        assert _builder.reinforcement_profile_type == reinforcement_profile_type
        assert isinstance(_builder, expected_builder)
        assert isinstance(_builder, ReinforcementProfileBuilderProtocol)

    @pytest.fixture(
        params=list(
            map(lambda x: pytest.param(x, id=x.case_name), reinforcement_profile_cases)
        ),
    )
    def reinforcement_profile_case(
        self, request: pytest.FixtureRequest
    ) -> ReinforcementProfileCase:
        _combination: ReinforcementProfileCaseCombination = request.param
        _base_input_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=_combination.input_profile_case,
                layers_data=_combination.koswat_layers_case.layers_dict,
                p4_x_coordinate=_combination.p4_x_coordinate,
            )
        ).build()

        if math.isnan(_combination.koswat_scenario_case.kruin_breedte):
            _combination.koswat_scenario_case.kruin_breedte = (
                _combination.input_profile_case.kruin_breedte
            )
        if math.isnan(_combination.koswat_scenario_case.buiten_talud):
            _combination.koswat_scenario_case.buiten_talud = (
                _combination.input_profile_case.buiten_talud
            )

        def _get_reinforced_profile() -> ReinforcementProfileProtocol:
            _reinforcement = _combination.reinforcement_profile_type()
            # Input profile data.
            _reinforcement.input_data = _combination.expectation.input_profile_base
            # Char points
            _char_points_builder = CharacteristicPointsBuilder()
            _char_points_builder.input_profile = _reinforcement.input_data
            _char_points_builder.p4_x_coordinate = (
                _combination.expectation.p4_x_coordinate
            )
            _reinforcement.characteristic_points = _char_points_builder.build()

            # layers
            def _get_layers(
                builder: KoswatLayersWrapperBuilderProtocol,
                layers_data: dict,
                char_points,
            ) -> KoswatLayersWrapperProtocol:
                builder.layers_data = layers_data
                builder.profile_points = char_points
                return builder.build()

            _layers_wrapper_builder: KoswatLayersWrapperBuilderProtocol = None
            if isinstance(_reinforcement, StandardReinforcementProfile):
                _layers_wrapper_builder = StandardReinforcementLayersWrapperBuilder()
            elif isinstance(_reinforcement, OutsideSlopeReinforcementProfile):
                _layers_wrapper_builder = (
                    OutsideSlopeReinforcementLayersWrapperBuilder()
                )

            _initial_layers_wrapper = _get_layers(
                KoswatLayersWrapperBuilder(),
                _combination.expectation.koswat_layers_case.layers_dict,
                _reinforcement.characteristic_points.points,
            )
            _reinforcement.layers_wrapper = _get_layers(
                _layers_wrapper_builder,
                _initial_layers_wrapper.as_data_dict(),
                _reinforcement.characteristic_points.points,
            )

            return _reinforcement

        _expected_reinforcement = _get_reinforced_profile()
        yield ReinforcementProfileCase(
            case_name=_combination.case_name,
            koswat_input_profile_base_case=_base_input_profile,
            koswat_scenario_case=_combination.koswat_scenario_case,
            reinforcement_profile_type=_combination.reinforcement_profile_type,
            expected_reinforcement_profile=_expected_reinforcement,
        )

    def test_given_profile_and_scenario_calculate_new_geometry_without_layers(
        self,
        reinforcement_profile_case: ReinforcementProfileCase,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _plot_dir = get_testcase_results_dir(request)

        # 2. Run test.
        _reinforcement_builder = ReinforcementProfileBuilderFactory.get_builder(
            reinforcement_profile_case.reinforcement_profile_type
        )
        _reinforcement_builder.base_profile = (
            reinforcement_profile_case.koswat_input_profile_base_case
        )
        _reinforcement_builder.scenario = (
            reinforcement_profile_case.koswat_scenario_case
        )
        _reinforcement_profile = _reinforcement_builder.build()

        # 3. Verify expectations.
        assert isinstance(
            _reinforcement_profile,
            reinforcement_profile_case.reinforcement_profile_type,
        )
        assert isinstance(_reinforcement_profile, ReinforcementProfileProtocol)
        assert isinstance(_reinforcement_profile, KoswatProfileProtocol)
        assert isinstance(
            _reinforcement_profile.input_data, ReinforcementInputProfileProtocol
        )
        validated_reinforced_profile(
            _reinforcement_profile,
            reinforcement_profile_case.expected_reinforcement_profile,
        )
        self._plot_profiles(
            reinforcement_profile_case.koswat_input_profile_base_case,
            _reinforcement_profile,
            _plot_dir,
        )

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
        profile_type: type[ReinforcementProfileProtocol],
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
