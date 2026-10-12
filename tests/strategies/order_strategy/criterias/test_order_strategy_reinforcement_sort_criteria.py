from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_crest_reinforcement_profile import (
    StabilityWallCrestReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_toe_reinforcement_profile import (
    StabilityWallToeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)
from koswat.strategies.strategy_reinforcement_input.flexible_strategy_reinforcement_input import (
    FlexibleStrategyReinforcementInput,
)
from koswat.strategies.order_strategy.criterias.order_strategy_reinforcement_sort_criteria import (
    OrderStrategyReinforcementSortCriteria,
)


class TestOrderStrategyReinforcementSortCriteria:
    """
    Test suite for the OrderStrategyReinforcementSortCriteria class.
    """

    def test_when_sort_given_unordered_strategies_sets_correct_order(self):
        # 1. Given
        _strategy_inputs = [
            FlexibleStrategyReinforcementInput(
                reinforcement_type=VPSReinforcementProfile,
                ground_level_surface=10,
                base_costs_with_surtax=1100,
            ),
            FlexibleStrategyReinforcementInput(
                reinforcement_type=StabilityWallCrestReinforcementProfile,
                ground_level_surface=15,
                base_costs_with_surtax=1000,
            ),
            FlexibleStrategyReinforcementInput(
                reinforcement_type=StabilityWallToeReinforcementProfile,
                ground_level_surface=10,
                base_costs_with_surtax=1000,
            ),
        ]

        # 2. When
        _sorted_strategies = OrderStrategyReinforcementSortCriteria(
            _strategy_inputs
        ).sort()

        # 3. Then
        assert (
            _sorted_strategies[0].reinforcement_type
            == StabilityWallCrestReinforcementProfile
        )
        assert _sorted_strategies[1].reinforcement_type == VPSReinforcementProfile
        assert (
            _sorted_strategies[2].reinforcement_type
            == StabilityWallToeReinforcementProfile
        )
