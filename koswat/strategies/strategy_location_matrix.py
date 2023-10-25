from dataclasses import dataclass
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyLocationReinforcements:
    location: PointSurroundings
    selected_measure: Type[ReinforcementProfileProtocol]
    available_measures: list[Type[ReinforcementProfileProtocol]]
