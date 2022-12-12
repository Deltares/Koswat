from shapely.geometry import Point

from koswat.calculations import ReinforcementProfileProtocol
from koswat.calculations.outside_slope_reinforcement import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.standard_reinforcement import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.configuration.models import KoswatScenario
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
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


class TestKoswatSummaryBuilder:
    def test_initialize(self):
        _builder = KoswatSummaryBuilder()
        assert isinstance(_builder, KoswatSummaryBuilder)
        assert not _builder.surroundings
        assert not _builder.base_profile
        assert not _builder.scenario

    def test_get_calculated_profile_list(self):
        # 1. Define test data.
        _expected_profile_types = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]
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
        _builder.surroundings = SurroundingsWrapper()

        # 2. Run test.
        _multi_location_profile_cost_builder = (
            _builder._get_multi_location_profile_cost_builder()
        )

        # 3. Verify expectations.
        assert isinstance(
            _multi_location_profile_cost_builder, MultiLocationProfileCostReportBuilder
        )
        assert (
            _multi_location_profile_cost_builder.surroundings == _builder.surroundings
        )
        assert not _multi_location_profile_cost_builder.reinforced_profile

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
