import pytest
from shapely.geometry import Point

from koswat.calculations.list_multi_location_profile_cost_builder import (
    ListMultiProfileCostBuilder,
)
from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.koswat_report import MultiLocationProfileCostReport
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder
from koswat.surroundings.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.surroundings.koswat_surroundings import KoswatSurroundings
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


class TestMultiLocationProfileCostBuilder:
    def test_initialize(self):
        _builder = ListMultiProfileCostBuilder()
        assert isinstance(_builder, ListMultiProfileCostBuilder)
        assert not _builder.surroundings
        assert not _builder.base_profile
        assert not _builder.scenario

    def test_get_calculated_profiles(self):
        # 1. Define test data.
        _builder = ListMultiProfileCostBuilder()
        _builder.scenario = KoswatScenario.from_dict(ScenarioCases.default)
        _builder.base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=0,
            )
        ).build(KoswatProfileBase)

        # 2. Run test.
        _calc_profiles = _builder._get_calculated_profiles()

        # 3. Verify expectations.
        assert len(_calc_profiles) == 1
        assert isinstance(_calc_profiles[0], ProfileReinforcement)

    def test_get_profile_cost_report_list(self):
        # 1. Define test data.
        _builder = ListMultiProfileCostBuilder()
        _builder.scenario = KoswatScenario.from_dict(ScenarioCases.default)
        _builder.surroundings = KoswatSurroundings()
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
            )
        ).build(KoswatProfileBase)

        # 2. Run test.
        _profile_cost_report_list = _builder._get_profile_cost_report_list()

        # 3. Verify expectations.
        assert len(_profile_cost_report_list) == 1
        assert isinstance(_profile_cost_report_list[0], MultiLocationProfileCostReport)
        assert _profile_cost_report_list[0].locations == [_p_surrounding]

    def test_build(self):
        # 1. Define test data.
        _builder = ListMultiProfileCostBuilder()
        _builder.scenario = KoswatScenario.from_dict(ScenarioCases.default)
        _builder.surroundings = KoswatSurroundings()
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
            )
        ).build(KoswatProfileBase)

        # 2. Run test.
        _profile_cost_report_list = _builder.build()

        # 3. Verify expectations.
        assert len(_profile_cost_report_list) == 1
        assert isinstance(_profile_cost_report_list[0], MultiLocationProfileCostReport)
        assert _profile_cost_report_list[0].locations == [_p_surrounding]
