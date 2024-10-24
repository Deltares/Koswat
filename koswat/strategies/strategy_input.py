from dataclasses import dataclass

from koswat.strategies.strategy_location_input import StrategyLocationInput


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocationInput]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
