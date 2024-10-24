from dataclasses import dataclass

from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocationInput]
    strategy_reinforcement_type_costs: list[StrategyReinforcementTypeCosts]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
