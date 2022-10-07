from shapely.geometry import Point

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_builder import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_builder import ProfileCostReportBuilder
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from koswat.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.surroundings.koswat_surroundings import KoswatSurroundings
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


class TestMultiLocationProfileCostReportBuilder:
    def test_initialize(self):
        _builder = MultiLocationProfileCostReportBuilder()
        assert isinstance(_builder, MultiLocationProfileCostReportBuilder)
        assert not _builder.surroundings
        assert not _builder.base_profile

    def test_get_profile_cost_builder(self):
        # 1. Define test data.
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.default,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=0,
            )
        ).build(KoswatProfileBase)
        _builder.calc_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.profile_case_2,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=3,
            )
        ).build(KoswatProfileBase)

        # 2. Run test.
        _profile_builder = _builder._get_profile_cost_builder()

        # 3. Verify expectations.
        assert isinstance(_profile_builder, ProfileCostReportBuilder)

    def test_build(self):
        # 1. Define test data.
        _builder = MultiLocationProfileCostReportBuilder()
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
        _builder.calc_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.profile_case_2,
                layers_data=LayersCases.without_layers,
                p4_x_coordinate=3,
            )
        ).build(KoswatProfileBase)

        # 2. Run test.
        _profile_cost_report = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_profile_cost_report, MultiLocationProfileCostReport)
        assert _profile_cost_report.locations == [_p_surrounding]