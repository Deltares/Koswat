from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementInput:
    reinforcement_type: type[ReinforcementProfileProtocol]
    base_costs: float = 0.0
    ground_level_surface: float = 0.0

    def __hash__(self) -> int:
        return hash(self.reinforcement_type)
