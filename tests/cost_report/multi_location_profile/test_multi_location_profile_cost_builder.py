from shapely.geometry import Point

from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_builder import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.surroundings_wrapper import (
    SurroundingsObstacle,
    SurroundingsWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.layers_cases import LayersCases


class TestMultiLocationProfileCostReportBuilder:
    def test_initialize(self):
        _builder = MultiLocationProfileCostReportBuilder()
        assert isinstance(_builder, MultiLocationProfileCostReportBuilder)
        assert not _builder.surroundings
        assert not _builder.reinforced_profile

    def test_build(self):
        # 1. Define test data.
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.surroundings = SurroundingsWrapper(
            apply_buildings=True,
        )
        _builder.koswat_costs_settings = KoswatCostsSettings()
        _p_surrounding = PointSurroundings()
        _p_surrounding.surroundings_matrix = {}
        _p_surrounding.location = Point(2.4, 4.2)
        _builder.surroundings.buildings_polderside.points = [_p_surrounding]
        _builder.reinforced_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.profile_case_2,
                layers_data=LayersCases.without_layers.layers_dict,
                p4_x_coordinate=3,
                reinforcement_type=CofferdamReinforcementProfile,
            )
        ).build()

        # 2. Run test.
        _profile_cost_report = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_profile_cost_report, MultiLocationProfileCostReport)
        assert any(_profile_cost_report.locations)
        assert _profile_cost_report.locations[0].location == _p_surrounding.location
