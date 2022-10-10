import math
from typing import List

from shapely.geometry import Point


class PointSurroundings:
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else).
    """

    section: str
    location: Point
    distance_to_buildings: List[float]

    def __init__(self) -> None:
        self.section = ""
        self.location = None
        self.distance_to_buildings = []

    @property
    def closest_building(self) -> float:
        return min(self.distance_to_buildings, default=math.nan)