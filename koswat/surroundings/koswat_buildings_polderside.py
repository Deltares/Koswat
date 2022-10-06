import math
from collections import defaultdict
from typing import Dict, List

from shapely.geometry import Point

from koswat.surroundings.surroundings_protocol import SurroundingsProtocol


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


class KoswatBuildingsPolderside(SurroundingsProtocol):
    points: List[PointSurroundings]

    def __init__(self) -> None:
        self.points = []

    @property
    def conflicting_points(self) -> List[PointSurroundings]:
        return [_cf for _cf in self.points if any(_cf.distance_to_buildings)]

    def get_classify_surroundings(self) -> Dict[float, List[PointSurroundings]]:
        """
        Gets all the `points` in a dictionary indexed by their closest distance to a building.

        Returns:
            Dict[float, List[PointSurroundings]]: Keys represent distance to a building, values are the points matching that criteria.
        """
        if not self.points:
            return {}
        _surroundings_dict = defaultdict(list)
        for ps in self.points:
            _surroundings_dict[ps.closest_building].append(ps.location)
        return _surroundings_dict

    def get_locations_after_distance(self, distance: float) -> List[Point]:
        def is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if not point_surroundings.distance_to_buildings:
                return True
            return distance < point_surroundings.distance_to_buildings[0]

        return list(filter(is_at_safe_distance, self.points))
