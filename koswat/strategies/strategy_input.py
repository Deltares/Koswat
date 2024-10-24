from dataclasses import dataclass

from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type import StrategyReinforcementType


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocationInput]
    reinforcements: list[StrategyReinforcementType]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
