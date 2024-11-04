import math
from dataclasses import dataclass, field

from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput


@dataclass
class StrategyInput:
    """
    Represents the input data structure for a strategy.
    """

    strategy_locations: list[StrategyLocationInput] = field(default_factory=lambda: [])
    strategy_reinforcements: list[StrategyReinforcementInput] = field(
        default_factory=lambda: []
    )
    reinforcement_min_buffer: float = 0.0
    reinforcement_min_length: float = 0.0

    @property
    def reinforcement_min_cluster(self) -> int:
        """
        Returns the minimum length of a reinforcement type
        along a traject, usually named as `cluster` throughout
        the code.

        Returns:
            int: `Total length`
        """
        if math.isnan(self.reinforcement_min_buffer):
            return -1
        return int(round(2 * self.reinforcement_min_buffer)) + 1
