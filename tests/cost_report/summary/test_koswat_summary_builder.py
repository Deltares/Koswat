from shapely.geometry import Point

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.soil.soil_reinforcement_profile import SoilReinforcementProfile
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
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.koswat_scenario import KoswatScenario
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


class TestKoswatSummaryBuilder:
    def test_initialize(self):
        _builder = KoswatSummaryBuilder()
        assert isinstance(_builder, KoswatSummaryBuilder)
        assert not _builder.surroundings
        assert not _builder.base_profile
        assert not _builder.scenario

    def test_get_calculated_profiles(self):
        # 1. Define test data.
        _builder = KoswatSummaryBuilder()
        _builder.scenario = KoswatScenario.from_dict(ScenarioCases.default)
        _builder.base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()

        # 2. Run test.
        _calc_profiles = _builder._get_calculated_profiles()

        # 3. Verify expectations.
        assert len(_calc_profiles) == 1
        assert all(
            isinstance(_calc_profile, ReinforcementProfileProtocol)
            for _calc_profile in _calc_profiles
        )
        assert isinstance(_calc_profiles[0], SoilReinforcementProfile)

    def test_get_multi_location_profile_cost_builder(self):
        # 1. Define test data.
        _builder = KoswatSummaryBuilder()
        _builder.surroundings = SurroundingsWrapper()
        _builder.base_profile = KoswatProfileBase()

        # 2. Run test.
        _multi_location_profile_cost_builder = (
            _builder._get_multi_location_profile_cost_builder()
        )

        # 3. Verify expectations.
        assert isinstance(
            _multi_location_profile_cost_builder, MultiLocationProfileCostReportBuilder
        )
        assert (
            _multi_location_profile_cost_builder.base_profile == _builder.base_profile
        )
        assert (
            _multi_location_profile_cost_builder.surroundings == _builder.surroundings
        )
        assert not _multi_location_profile_cost_builder.calc_profile

    def test_build(self):
        # 1. Define test data.
        _builder = KoswatSummaryBuilder()
        _builder.scenario = KoswatScenario.from_dict(ScenarioCases.default)
        _builder.surroundings = SurroundingsWrapper()
        _p_surrounding = PointSurroundings()
        _p_surrounding.distance_to_buildings = []
        _p_surrounding.location = Point(2.4, 4.2)
        _builder.surroundings.buldings_polderside = KoswatBuildingsPolderside()
        _builder.surroundings.buldings_polderside.points = [_p_surrounding]
        _builder.base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=0,
                profile_type=KoswatProfileBase,
            )
        ).build()

        # 2. Run test.
        _summary = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_summary, KoswatSummary)
        assert any(_summary.locations_profile_report_list)
        assert all(
            isinstance(lpr, MultiLocationProfileCostReport)
            for lpr in _summary.locations_profile_report_list
        )
        assert _summary.locations_profile_report_list[0].locations == [_p_surrounding]
