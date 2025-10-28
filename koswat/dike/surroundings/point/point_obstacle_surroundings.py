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

    @property
    def closest_obstacle(self) -> float:
        """
        Distance to the closest (obstacle) surrounding. When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """

        return self.inside_distance