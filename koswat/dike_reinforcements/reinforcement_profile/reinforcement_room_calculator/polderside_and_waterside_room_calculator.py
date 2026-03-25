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
from dataclasses import dataclass
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator import ReinforcementRoomCalculatorBase

@dataclass
class PoldersideAndWatersideRoomCalculator(ReinforcementRoomCalculatorBase):
    required_polderside_width: float
    required_waterside_width: float

    @property
    def _required_width(self) -> float:
        return self.required_polderside_width + self.required_waterside_width

    def reinforcement_has_room(self, point_obstacle_surroundings: PointObstacleSurroundings) -> bool:
        return self._required_width_less_or_equal(
            point_obstacle_surroundings.inside_distance 
            + point_obstacle_surroundings.outside_distance)