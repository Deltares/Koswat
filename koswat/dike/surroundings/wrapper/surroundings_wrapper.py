import copy
import logging
import math
from collections import defaultdict
from dataclasses import dataclass

from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
)


@dataclass
class SurroundingsWrapper:
    dike_section: str = ""
    traject: str = ""
    subtraject: str = ""
    apply_waterside: bool = False
    apply_buildings: bool = False
    apply_railways: bool = False
    apply_waters: bool = False

    reinforcement_min_separation: float = float("nan")
    reinforcement_min_buffer: float = float("nan")

    buildings_polderside: KoswatSurroundingsPolderside = None
    buildings_dikeside: KoswatSurroundingsProtocol = None

    railways_polderside: KoswatSurroundingsPolderside = None
    railways_dikeside: KoswatSurroundingsProtocol = None

    waters_polderside: KoswatSurroundingsPolderside = None
    waters_dikeside: KoswatSurroundingsProtocol = None

    roads_class_2_polderside: KoswatSurroundingsProtocol = None
    roads_class_7_polderside: KoswatSurroundingsProtocol = None
    roads_class_24_polderside: KoswatSurroundingsProtocol = None
    roads_class_47_polderside: KoswatSurroundingsProtocol = None
    roads_class_unknown_polderside: KoswatSurroundingsProtocol = None

    roads_class_2_dikeside: KoswatSurroundingsProtocol = None
    roads_class_7_dikeside: KoswatSurroundingsProtocol = None
    roads_class_24_dikeside: KoswatSurroundingsProtocol = None
    roads_class_47_dikeside: KoswatSurroundingsProtocol = None
    roads_class_unknown_dikeside: KoswatSurroundingsProtocol = None

    @property
    def locations(self) -> list[PointSurroundings]:
        """
        Overlay of locations of the different surroundings that are present.
        Buildings need to be present as input (leading for location coordinates).
        Each location represents 1 meter in a real scale map.

        Returns:
            List[PointSurroundings]: List of points along the polderside.
        """

        def _match_locations(
            point1: PointSurroundings, point2: PointSurroundings
        ) -> dict[float, float]:
            if point1.location != point2.location:
                logging.warning(
                    f"Mismatching railway polderside location {point2.location}"
                )
            _matched_locations_dict = defaultdict(lambda: 0)
            for _key, _value in point1.distance_to_surroundings_dict.items():
                _matched_locations_dict[_key] += _value
            return _matched_locations_dict

        if not self.buildings_polderside:
            return []

        _points = copy.deepcopy(self.buildings_polderside.points)

        for _p, _point in enumerate(_points):
            if not self.apply_buildings:
                _points[_p].distance_to_surroundings_dict = {}

            if self.apply_railways and self.railways_polderside:
                _points[_p].distance_to_surroundings_dict = _match_locations(
                    _point, self.railways_polderside.points[_p]
                )

            if self.apply_waters and self.waters_polderside:
                _points[_p].distance_to_surroundings_dict = _match_locations(
                    _point, self.waters_polderside.points[_p]
                )

        return _points

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
