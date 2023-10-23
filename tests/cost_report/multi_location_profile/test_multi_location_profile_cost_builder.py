from shapely.geometry import Point

from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_builder_factory import (
    ReinforcementProfileBuilderFactory,
)
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_builder import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
    PointSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.koswat_scenario_test_cases import ScenarioCases
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
        _builder.surroundings = SurroundingsWrapper()
        _builder.koswat_costs = KoswatCostsSettings()
        _p_surrounding = PointSurroundings()
        _p_surrounding.distance_to_surroundings = []
        _p_surrounding.location = Point(2.4, 4.2)
        _builder.surroundings.buildings_polderside = KoswatSurroundingsPolderside()
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
        assert _profile_cost_report.locations[0].location == _p_surrounding.location
