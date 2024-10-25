from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementTypeCosts:
    reinforcement_type: type[ReinforcementProfileProtocol]
    base_costs: float = 0.0
    infrastructure_costs: float = 0.0

    @property
    def total_costs(self) -> float:
        """
        The simple addition of the base costs and the possible
        related infrastructure costs.
        Returns:
            float: The total costs when applying this reinforcement.
        """
        return self.base_costs + self.infrastructure_costs
