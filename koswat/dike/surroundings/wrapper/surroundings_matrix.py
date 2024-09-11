import math
from collections import defaultdict
from dataclasses import dataclass, field

from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class PointSurroundingsTypeMatrix:
    """
    Represents all the surroundings at a given location.
    """

    buildings: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )
    railways: dict[float, float] = field(default_factory=lambda: defaultdict(lambda: 0))
    waters: dict[float, float] = field(default_factory=lambda: defaultdict(lambda: 0))

    roads_class_2: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )
    roads_class_7: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )
    roads_class_24: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )
    roads_class_47: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )
    roads_class_unknown: dict[float, float] = field(
        default_factory=lambda: defaultdict(lambda: 0)
    )

    def get_locations_after_distance(self, distance: float) -> list[Point]:
        """
        Gets all locations which are safe from surroundings (building/railway/water) in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[Point]: List of safe locations (points).
        """

        def _is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if math.isnan(point_surroundings.closest_surrounding):
                return True
            return distance < point_surroundings.closest_surrounding

        return list(filter(_is_at_safe_distance, self.locations))
