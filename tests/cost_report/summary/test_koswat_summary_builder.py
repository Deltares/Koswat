from shapely.geometry import Point

from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_builder import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.cost_report.summary.koswat_summary_builder import KoswatSummaryBuilder
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
    PointSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.koswat_scenario_test_cases import ScenarioCases
from tests.acceptance_scenarios.layers_cases import LayersCases


class TestKoswatSummaryBuilder:
    def test_initialize(self):
        _builder = KoswatSummaryBuilder()
        assert isinstance(_builder, KoswatSummaryBuilder)
        assert not _builder.run_scenario_settings

    def test_get_calculated_profile_list(self):
        # 1. Define test data.
        _expected_profile_types = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]
        _builder = KoswatSummaryBuilder()
        _settings = KoswatRunScenarioSettings()
        _settings.scenario = ScenarioCases.default
        _settings.reinforcement_settings = KoswatReinforcementSettings()
        _settings.input_profile_case = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers.layers_dict,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()
        _builder.run_scenario_settings = _settings

        # 2. Run test.
        _calc_profiles = _builder._get_calculated_profile_list()

        # 3. Verify expectations.
        assert any(_calc_profiles)
        assert all(
            isinstance(_calc_profile, ReinforcementProfileProtocol)
            for _calc_profile in _calc_profiles
        )

        for _required_profile in _expected_profile_types:
            assert any(
                isinstance(_calc_prof, _required_profile)
                for _calc_prof in _calc_profiles
            ), f"Profile {_required_profile} not found."

    def test_get_multi_location_profile_cost_builder(self):
        # 1. Define test data.
        _builder = KoswatSummaryBuilder()
        _settings = KoswatRunScenarioSettings()
        _settings.surroundings = SurroundingsWrapper()
        _settings.costs_setting = KoswatCostsSettings()
        _builder.run_scenario_settings = _settings

        # 2. Run test.
        _multi_location_profile_cost_builder = (
            _builder._get_multi_location_profile_cost_builder()
        )

        # 3. Verify expectations.
        assert isinstance(
            _multi_location_profile_cost_builder, MultiLocationProfileCostReportBuilder
        )
        assert (
            _multi_location_profile_cost_builder.surroundings == _settings.surroundings
        )
        assert not _multi_location_profile_cost_builder.reinforced_profile

    def test_build(self):
        # 1. Define test data.
        _builder = KoswatSummaryBuilder()
        _run_settings = KoswatRunScenarioSettings()
        _run_settings.scenario = ScenarioCases.default
        _run_settings.reinforcement_settings = KoswatReinforcementSettings()
        _run_settings.surroundings = SurroundingsWrapper()
        _run_settings.costs_setting = KoswatCostsSettings()
        _p_surrounding = PointSurroundings()
        _p_surrounding.distance_to_surroundings = []
        _p_surrounding.location = Point(2.4, 4.2)
        _run_settings.surroundings.buildings_polderside = KoswatSurroundingsPolderside()
        _run_settings.surroundings.buildings_polderside.points = [_p_surrounding]
        _run_settings.surroundings.reinforcement_min_buffer = 10
        _run_settings.surroundings.reinforcement_min_separation = 50
        _run_settings.input_profile_case = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers.layers_dict,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()
        _builder.run_scenario_settings = _run_settings

        # 2. Run test.
        _summary = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_summary, KoswatSummary)
        assert any(_summary.locations_profile_report_list)
        assert all(
            isinstance(lpr, MultiLocationProfileCostReport)
            for lpr in _summary.locations_profile_report_list
        )
        assert (
            _summary.locations_profile_report_list[0].locations[0].location
            == _p_surrounding.location
        )
