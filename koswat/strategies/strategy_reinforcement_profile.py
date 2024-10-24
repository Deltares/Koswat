from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementProfile:
    """
    Contains the relevant information for a reinforcement profile in a strategy.
    """

    reinforcement_type: type[ReinforcementProfileProtocol]
    ground_level_surface: float
    total_cost: float
