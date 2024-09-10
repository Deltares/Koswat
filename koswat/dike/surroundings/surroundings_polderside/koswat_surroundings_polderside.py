import math
from collections import defaultdict

from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatSurroundingsPolderside(KoswatSurroundingsProtocol):
    points: list[PointSurroundings]

    def __init__(self) -> None:
        self.points = []

    @property
    def conflicting_points(self) -> list[PointSurroundings]:
        """
        TODO: Seems unused, remove when possible
        """
        return [_cf for _cf in self.points if any(_cf.surroundings_distances)]

    def get_classify_surroundings(self) -> dict[float, list[PointSurroundings]]:
        """
        Gets all the `points` in a dictionary indexed by their closest distance to a surrounding.

        Returns:
            dict[float, list[PointSurroundings]]: Keys represent distance to a surrounding, values are the points matching that criteria.
        """
        if not self.points:
            return {}
        _surroundings_dict = defaultdict(list)
        for ps in self.points:
            _surroundings_dict[ps.closest_surrounding].append(ps.location)
        return _surroundings_dict

    def get_locations_after_distance(self, distance: float) -> list[Point]:
        """
        Gets all points which do not contain any surrounding between their position and a radius of `distance` meters.

        Args:
            distance (float): Radius from a coordinate where to check for surroundings.

        Returns:
            list[Point]: List of points which do not contain any surroundings for the provided distance.
        """

        def _is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if math.isnan(point_surroundings.closest_surrounding):
                return True
            return distance < point_surroundings.closest_surrounding

        return list(filter(_is_at_safe_distance, self.points))
