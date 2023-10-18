import math
from typing import List

from shapely.geometry import Point


class PointSurroundings:
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else).
    """

    section: str
    traject_order: int
    location: Point
    distance_to_surroundings: List[float]

    def __init__(self) -> None:
        self.section = ""
        self.location = None
        self.traject_order = -1
        self.distance_to_surroundings = []

    @property
    def closest_surrounding(self) -> float:
        """
        Distance to the closest surrounding (building/railway/water). When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """
        return min(self.distance_to_surroundings, default=math.nan)
