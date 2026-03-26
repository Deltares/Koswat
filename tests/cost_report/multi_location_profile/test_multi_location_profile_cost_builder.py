import math

from shapely.geometry import Point
from sklearn import base

from koswat.configuration.settings.costs.dike_profile_costs_settings import DikeProfileCostsSettings
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
from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import ReinforcementProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_base import ReinforcementRoomCalculatorBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import ReinforcementRoomCalculatorProtocol
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile_builder import StandardReinforcementProfileBuilder
from tests.acceptance_scenarios.koswat_input_profile_base_cases import InputProfileCases
from tests.acceptance_scenarios.layers_cases import LayersCases


class TestMultiLocationProfileCostReportBuilder:
    def test_initialize(self):
        _builder = MultiLocationProfileCostReportBuilder()
        assert isinstance(_builder, MultiLocationProfileCostReportBuilder)
        assert not _builder.surroundings
        assert not _builder.reinforced_profile

    def test_when_build_given_mocked_reinforced_profile_then_returns_expected_locations(self):
        # 1. Define test data.
        _builder = MultiLocationProfileCostReportBuilder()

        # Define surroundings
        _builder.surroundings = SurroundingsWrapper()
        _p_surrounding = PointObstacleSurroundings(
            inside_distance=math.nan,
            outside_distance=math.nan,
            location=Point(2.4, 4.2),
        )
        _builder.surroundings.obstacle_surroundings_wrapper.obstacles.points = [
            _p_surrounding
        ]

        # Create a 'mocked' reinforcement profile.
        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=InputProfileCases.profile_case_2,
                layers_data=LayersCases.without_layers.layers_dict,
                p4_x_coordinate=3,
                reinforcement_type=CofferdamReinforcementProfile,
            )
        ).build()
       
        class DummyReinforcedProfile(ReinforcementProfileProtocol):
            old_profile = None
            layers_wrapper = _base_profile.layers_wrapper
            def get_reinforcement_room_calculator(self):
                class DummyReinforcementRoomCalculator(ReinforcementRoomCalculatorProtocol):
                    def reinforcement_has_room(self, *args):
                        return True
                return DummyReinforcementRoomCalculator()
            
        _builder.reinforced_profile = DummyReinforcedProfile()

        # Define costs
        _builder.koswat_costs_settings = KoswatCostsSettings()
        _builder.koswat_costs_settings.dike_profile_costs = DikeProfileCostsSettings()


        # 2. Run test.
        _profile_cost_report = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_profile_cost_report, MultiLocationProfileCostReport)
        assert any(_profile_cost_report.report_locations)
        assert (
            _profile_cost_report.report_locations[0].location == _p_surrounding.location
        )
