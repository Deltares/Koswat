from dataclasses import dataclass

from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocationInput]
    strategy_reinforcements: list[StrategyReinforcementInput]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
