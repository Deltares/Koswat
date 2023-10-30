from dataclasses import dataclass
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyInput:
    locations_matrix: dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
