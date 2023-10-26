from dataclasses import dataclass
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyInput:
    locations_matrix: dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]
    structure_buffer: float
    min_space_between_structures: float
