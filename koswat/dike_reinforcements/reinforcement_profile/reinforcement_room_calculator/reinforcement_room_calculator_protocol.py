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

from typing import Protocol, runtime_checkable

from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)


@runtime_checkable
class ReinforcementRoomCalculatorProtocol(Protocol):
    def reinforcement_has_room(
        self, point_obstacle_surroundings: PointObstacleSurroundings
    ) -> bool:
        """
        Checks if there is enough room for a given reinforcement at a given point with obstacles.

        Args:
            point_obstacle_surroundings (PointObstacleSurroundings): The point surroundings to check.

        Returns:
            bool: True if there is enough room for reinforcement, False otherwise.
        """
        pass
