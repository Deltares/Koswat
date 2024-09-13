import math
from dataclasses import dataclass, field

from shapely import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsObstacle(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that cannot be repaired or replaced.
    The `PointSurroundings` contain a matrix (dictionary) where the keys
    represent the distances to an obstacle, and the values a `1` (obstacle present)
    or a `0` (obstacle not present).
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])

    def get_locations_after_distance(self, distance: float) -> list[Point]:
        """
        Gets all points which do not contain any surrounding between their position and a radius of `distance` meters.

        Args:
            distance (float): Radius from a coordinate where to check for surroundings.

        Returns:
            list[Point]: List of points which do not contain any surroundings for the provided distance.
        """

        def _is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if math.isnan(point_surroundings.closest_obstacle):
                return True
            return distance < point_surroundings.closest_obstacle

        return list(filter(_is_at_safe_distance, self.points))
