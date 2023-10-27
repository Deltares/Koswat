from dataclasses import dataclass
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class StrategyInput:
    locations_matrix: dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]
    structure_min_buffer: float
    structure_min_length: float
