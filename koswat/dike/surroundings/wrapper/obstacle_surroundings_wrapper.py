"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
from dataclasses import dataclass, field

from koswat.dike.surroundings.point import PointObstacleSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator import (
    ReinforcementRoomCalculatorProtocol,
)


@dataclass
class ObstacleSurroundingsWrapper:
    reinforcement_min_separation: float = math.nan
    reinforcement_min_buffer: float = math.nan

    obstacles: SurroundingsObstacle = field(default_factory=SurroundingsObstacle)

    def get_locations_at_safe_distance(
        self, room_calculator: ReinforcementRoomCalculatorProtocol
    ) -> list[PointObstacleSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            room_calculator (ReinforcementRoomCalculatorProtocol): Calculator to determine if there is enough room for reinforcement at a given point.

        Returns:
            list[PointObstacleSurroundings]: List of safe locations (points with surroundings).
        """

        def _is_at_safe_distance(point_surroundings: PointObstacleSurroundings) -> bool:
            return room_calculator.reinforcement_has_room(point_surroundings)

        return list(filter(_is_at_safe_distance, self.obstacles.points))
