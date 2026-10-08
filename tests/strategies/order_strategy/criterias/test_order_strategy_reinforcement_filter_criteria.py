from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.order_strategy.criterias.order_strategy_reinforcement_filter_criteria import (
    OrderStrategyReinforcementFilterCriteria,
)
from koswat.strategies.strategy_input import StrategyInput


class TestOrderStrategyReinforcementFilterCriteria:

    def test_when_filter_given_less_cost_space_efficient_then_filters_out(
        self, example_strategy_input: list[StrategyInput]
    ):
        # 1. Define test data.
        _subset = example_strategy_input.strategy_reinforcements

        # Set first and last reinforcements 'unrealistic' to ensure they are not filtered out.
        _subset[0].ground_level_surface *= 1000
        _subset[0].base_costs_with_surtax *= 10
        _subset[-1].ground_level_surface *= 1000
        _subset[-1].base_costs_with_surtax *= 10

        # Set the 3rd reinforcement more expensive and equally restrictive than the 2nd reinforcement, so it should be filtered out.
        _subset[2].ground_level_surface = _subset[1].ground_level_surface
        _subset[2].base_costs_with_surtax = _subset[1].base_costs_with_surtax + 1
        _expected_result = (
            example_strategy_input.strategy_reinforcements[:2] + _subset[3:]
        )

        # 2. Run test.
        _filtered_reinforcements = OrderStrategyReinforcementFilterCriteria(
            example_strategy_input.strategy_reinforcements
        ).filter()

        # 3. Verify expectations
        assert _filtered_reinforcements == _expected_result
        assert (
            _filtered_reinforcements[0].reinforcement_type == SoilReinforcementProfile
        )
        assert (
            _filtered_reinforcements[-1].reinforcement_type
            == CofferdamReinforcementProfile
        )

    def test_when_filter_given_increased_surface_filters_reinforcement_then_filters_out(
        self,
        example_strategy_input: list[StrategyInput],
    ):
        # 1. Define test data.
        # Increase the surface of the reinforcement at the given index
        # to become more restrictive than the previous (cheaper) reinforcement
        # and will be filtered out.
        _subset = example_strategy_input.strategy_reinforcements
        _subset[2].ground_level_surface += 15
        _expected_result = (
            example_strategy_input.strategy_reinforcements[:2] + _subset[3:]
        )

        # 2. Run test.
        _filtered_reinforcements = OrderStrategyReinforcementFilterCriteria(
            example_strategy_input.strategy_reinforcements
        ).filter()

        # 3. Verify expectations
        assert _filtered_reinforcements == _expected_result
        assert (
            _filtered_reinforcements[0].reinforcement_type == SoilReinforcementProfile
        )
        assert (
            _filtered_reinforcements[-1].reinforcement_type
            == CofferdamReinforcementProfile
        )
