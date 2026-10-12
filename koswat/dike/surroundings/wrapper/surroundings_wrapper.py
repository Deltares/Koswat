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
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator import (
    ReinforcementRoomCalculatorProtocol,
)


@dataclass
class SurroundingsWrapper:
    dike_section: str = ""
    traject: str = ""
    subtraject: str = ""
    max_polderside_width_extension: float = float("nan")
    max_waterside_width_extension: float = float("nan")

    obstacle_surroundings_wrapper: ObstacleSurroundingsWrapper = field(
        default_factory=ObstacleSurroundingsWrapper
    )
    infrastructure_surroundings_wrapper: InfrastructureSurroundingsWrapper = field(
        default_factory=InfrastructureSurroundingsWrapper
    )

    def supports_reinforcement_width(
        self, reinforcement: ReinforcementProfileProtocol
    ) -> bool:
        """
        Determines if a reinforcement would fit given these surroundings wrapper.

        Args:
            reinforcement (ReinforcementProfileProtocol): Reinforcement to analyze.

        Returns:
            bool: the criteria result
        """

        def _compare_widths(reinforcement_width: float, max_width: float) -> bool:
            if float.isnan(max_width):
                return True
            return reinforcement_width <= max_width

        return _compare_widths(
            reinforcement.waterside_width, self.max_waterside_width_extension
        ) and _compare_widths(
            reinforcement.polderside_width, self.max_polderside_width_extension
        )

    def get_locations_at_safe_distance(
        self, room_calculator: ReinforcementRoomCalculatorProtocol
    ) -> list[PointSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[PointSurroundings]: List of safe locations (points with surroundings).
        """
        return self.obstacle_surroundings_wrapper.get_locations_at_safe_distance(
            room_calculator
        )
