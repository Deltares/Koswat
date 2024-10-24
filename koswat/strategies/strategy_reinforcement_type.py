from dataclasses import dataclass
from typing import Type

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementType:
    reinforcement_type: Type[ReinforcementProfileProtocol]
    base_costs: float = 0.0
    infastructure_costs: float = 0.0
    ground_level_surface: float = 0.0

    def __hash__(self) -> int:
        """
        Overriding of the "magic" hash operator required
        so that `StrategyReinforcementType` can be used as a key in a python dict or set.
        """
        return hash((self.reinforcement_type))

    @property
    def total_costs(self) -> float:
        """
        The simple addition of the base costs and the possible
        related infrastructure costs.
        Returns:
            float: The total costs when applying this reinforcement.
        """
        return self.base_costs + self.infastructure_costs
