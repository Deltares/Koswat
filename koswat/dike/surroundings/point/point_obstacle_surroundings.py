"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations
import math
from dataclasses import dataclass
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class PointObstacleSurroundings(PointSurroundings):
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else),
    extended with obstacle specific properties.
    """

    inside_distance: float = math.nan
    outside_distance: float = math.nan
    angle_inside: float = math.nan
    angle_outside: float = math.nan

    def __hash__(self):
        """
        Overriding of the "magic" hash operator required
        so that `PointObstacleSurroundings` can be used as a key in a python dict.
        It cannot be inherited from the parent class as the child class adds new properties.
        """
        return hash((self.section, self.traject_order, self.location))

    def merge(self, other: PointObstacleSurroundings) -> None:
        def _get_min_value(value_1: float, value_2: float) -> float:
            if math.isnan(value_1):
                return value_2
            if math.isnan(value_2):
                return value_1
            return min(value_1, value_2)

        self.inside_distance = _get_min_value(self.inside_distance, other.inside_distance)
        self.outside_distance = _get_min_value(self.outside_distance, other.outside_distance)
        self.angle_inside = _get_min_value(self.angle_inside, other.angle_inside)
        self.angle_outside = _get_min_value(self.angle_outside, other.angle_outside)

    @property
    def closest_obstacle(self) -> float:
        """
        Distance to the closest (obstacle) surrounding. When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """

        return self.inside_distance