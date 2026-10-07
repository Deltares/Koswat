from koswat.strategies.strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
    StrategyReinforcementInputBase,
)


class OrderStrategyReinforcementFilterCriteria:
    """
    Class to compare two reinforcement strategies based on their costs.

    Attributes:
        strategy_a (StrategyReinforcementInputBase): The first reinforcement strategy.
        strategy_b (StrategyReinforcementInputBase): The second reinforcement strategy.
    """

    def __init__(
        self,
        strategy_a: StrategyReinforcementInputBase,
        strategy_b: StrategyReinforcementInputBase,
    ):
        """
        Initialize the comparer with two reinforcement strategies.

        Args:
            strategy_a (StrategyReinforcementInputBase): The first reinforcement strategy.
            strategy_b (StrategyReinforcementInputBase): The second reinforcement strategy.
        """
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b

    def can_be_filtered_out(self) -> bool:
        """
        Compare the two strategies based on their total costs.

        Returns:
            bool: True if strategy_a can be filtered out by strategy_b, False otherwise.
        """
        if isinstance(self.strategy_a, FixedStrategyReinforcementInput) or isinstance(
            self.strategy_b, FixedStrategyReinforcementInput
        ):
            return False
        return self.strategy_a.is_filtered_out_by(self.strategy_b)
