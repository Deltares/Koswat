from typing import Protocol

from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class StrategyProtocol(Protocol):
    def apply_strategy(
        strategy_input: StrategyInput,
    ) -> list[StrategyLocationReinforcement]:
        """
        Applies a specific strategy by matching each location (`PointSurroundings`)
         to a valid reinforcement type (`ReinforcementProfileProtocol`).

        Args:
            strategy_input (`StrategyInput`): Input data structure containing locations and available reinforcements for each of them.

        Returns:
            list[StrategyLocationReinforcement]: List of mapped locations to applied reinforcement.
        """
        pass
