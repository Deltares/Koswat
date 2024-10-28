import math
from dataclasses import dataclass

from koswat.strategies.strategy_location_input import StrategyLocationInput


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocationInput]
    reinforcement_min_buffer: float
    reinforcement_min_length: float

    @property
    def reinforcement_min_cluster(self) -> int:
        """
        Returns the minimun length of a reinforcement type
        along a traject, usually named as `cluster` throughout
        the code.

        Returns:
            int: `Total length`
        """
        if math.isnan(self.reinforcement_min_buffer):
            return -1
        return int(round(2 * self.reinforcement_min_buffer)) + 1
