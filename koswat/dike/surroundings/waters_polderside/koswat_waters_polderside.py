from collections import defaultdict
from typing import Dict, List

from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatWatersPolderside(KoswatSurroundingsProtocol):
    points: List[PointSurroundings]

    def __init__(self) -> None:
        self.points = []

    @property
    def conflicting_points(self) -> List[PointSurroundings]:
        return [_cf for _cf in self.points if any(_cf.distance_to_water)]

    def get_classify_surroundings(self) -> Dict[float, List[PointSurroundings]]:
        """
        Gets all the `points` in a dictionary indexed by their closest distance to a water.

        Returns:
            Dict[float, List[PointSurroundings]]: Keys represent distance to a water, values are the points matching that criteria.
        """
        if not self.points:
            return {}
        _surroundings_dict = defaultdict(list)
        for ps in self.points:
            _surroundings_dict[ps.closest_water].append(ps.location)
        return _surroundings_dict

    def get_locations_after_distance(self, distance: float) -> List[Point]:
        """
        Gets all points which do not contain any water between their position and a radius of `distance` meters.

        Args:
            distance (float): Radius from a coordinate where to check for waters.

        Returns:
            List[Point]: List of points which do not contain any water for the provided distance.
        """

        def is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if not point_surroundings.distance_to_waters:
                return True
            return distance < point_surroundings.distance_to_waters[0]

        return list(filter(is_at_safe_distance, self.points))
