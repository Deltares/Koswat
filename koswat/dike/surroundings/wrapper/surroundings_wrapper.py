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

from dataclasses import dataclass, field

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)


@dataclass
class SurroundingsWrapper:
    dike_section: str = ""
    traject: str = ""
    subtraject: str = ""

    obstacle_surroundings_wrapper: ObstacleSurroundingsWrapper = field(
        default_factory=ObstacleSurroundingsWrapper
    )
    infrastructure_surroundings_wrapper: InfrastructureSurroundingsWrapper = field(
        default_factory=InfrastructureSurroundingsWrapper
    )

    def get_locations_at_safe_distance(
        self, distance: float
    ) -> list[PointSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[PointSurroundings]: List of safe locations (points with surroundings).
        """
        return self.obstacle_surroundings_wrapper.get_locations_at_safe_distance(
            distance
        )
