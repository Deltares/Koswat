from dataclasses import dataclass, field

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class StrategyOutput:
    """
    Represents the output data structure for a strategy.
    """

    location_reinforcements: list[StrategyLocationReinforcement] = field(
        default_factory=lambda: []
    )
    reinforcement_order: list[type[ReinforcementProfileProtocol]] = field(
        default_factory=lambda: []
    )
