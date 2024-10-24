from typing import Protocol, runtime_checkable

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.order_strategy.order_strategy_reinforcements import (
    StrategyReinforcementType,
)


@runtime_checkable
class StrategyReinforcementsProtocol(Protocol):
    reinforcements: list[StrategyReinforcementType]
    """
    Protocol to provide the reinforcements to be considered in the strategy.
    """

    @property
    def strategy_reinforcements(self) -> list[type[ReinforcementProfileProtocol]]:
        """
        Get the order in which the reinforcements should be considered.

        Returns:
            list[type[ReinforcementProfileProtocol]]: Order of reinforcements.
        """
