from koswat.strategies.strategy_reinforcement_input.fixed_strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
)
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_builder import (
    StrategyReinforcementInputBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile import SoilReinforcementProfile


class TestStrategyReinforcementInputBuilder:

    def test_when_build_given_soil_reinforcement_profile_then_returns_fixed_strategy_reinforcement_input(
        self,
    ):
        # 1. Define test data
        builder = StrategyReinforcementInputBuilder(
            reinforcement_type=SoilReinforcementProfile,
            active=True,
            base_costs_with_surtax=100.0,
            ground_level_surface=5.0,
        )

        # 2. When
        result = builder.build()

        # 3. Then
        assert isinstance(result, FixedStrategyReinforcementInput)
        assert result.reinforcement_type == SoilReinforcementProfile
        assert result.active == builder.active
        assert result.base_costs_with_surtax == builder.base_costs_with_surtax
        assert result.ground_level_surface == builder.ground_level_surface
