from typing import Protocol, runtime_checkable

from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_output import StrategyOutput


@runtime_checkable
class StrategyProtocol(Protocol):
    def apply_strategy(
        self,
        strategy_input: StrategyInput,
    ) -> StrategyOutput:
        """
        Applies a specific strategy by matching each location (`PointSurroundings`)
         to a valid reinforcement type (`ReinforcementProfileProtocol`).

        Args:
            strategy_input (`StrategyInput`): Input data structure containing locations and available reinforcements for each of them.

        Returns:
            StrategyOutput: Output data structure containing the selected reinforcements for each location.
        """
