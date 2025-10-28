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
        self.inside_distance = min(self.inside_distance, other.inside_distance)
        self.outside_distance = min(self.outside_distance, other.outside_distance)
        self.angle_inside = min(self.angle_inside, other.angle_inside)
        self.angle_outside = min(self.angle_outside, other.angle_outside)

    @property
    def closest_obstacle(self) -> float:
        """
        Distance to the closest (obstacle) surrounding. When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """

        return self.inside_distance