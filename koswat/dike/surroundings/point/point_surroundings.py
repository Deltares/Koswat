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
    distance_to_buildings: List[float]
    distance_to_railways: List[float]
    distance_to_waters: List[float]

    def __init__(self) -> None:
        self.section = ""
        self.location = None
        self.traject_order = -1
        self.distance_to_buildings = []
        self.distance_to_railways = []
        self.distance_to_waters = []

    @property
    def closest_building(self) -> float:
        """
        Distance to the closest building. When no buildings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest building.
        """
        return min(self.distance_to_buildings, default=math.nan)
    
    @property
    def closest_railway(self) -> float:
        """
        Distance to the closest railway. When no railways are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for railway at distance 0.

        Returns:
            float: Distance to the closest railway.
        """
        return min(self.distance_to_railways, default=math.nan)
    
    @property
    def closest_water(self) -> float:
        """
        Distance to the closest water. When no waters are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for waters at distance 0.

        Returns:
            float: Distance to the closest water.
        """
        return min(self.distance_to_waters, default=math.nan)
