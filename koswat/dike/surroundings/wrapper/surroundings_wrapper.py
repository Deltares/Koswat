import math
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain, groupby

from click import group
from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsObstacle(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that cannot be removed.
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])

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


@dataclass
class SurroundingsInfrastructure(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that can be removed or reworked.
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])

    pass


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

    buildings_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsObstacle
    )
    buildings_dikeside: KoswatSurroundingsProtocol = None

    railways_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsObstacle
    )
    railways_dikeside: KoswatSurroundingsProtocol = None

    waters_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsObstacle
    )
    waters_dikeside: KoswatSurroundingsProtocol = None

    roads_class_2_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsInfrastructure
    )
    roads_class_7_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsInfrastructure
    )
    roads_class_24_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsInfrastructure
    )
    roads_class_47_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsInfrastructure
    )
    roads_class_unknown_polderside: KoswatSurroundingsProtocol = field(
        default_factory=SurroundingsInfrastructure
    )

    roads_class_2_dikeside: KoswatSurroundingsProtocol = None
    roads_class_7_dikeside: KoswatSurroundingsProtocol = None
    roads_class_24_dikeside: KoswatSurroundingsProtocol = None
    roads_class_47_dikeside: KoswatSurroundingsProtocol = None
    roads_class_unknown_dikeside: KoswatSurroundingsProtocol = None

    @property
    def surroundings_collection(self) -> list[KoswatSurroundingsProtocol]:
        """
        The collection of `KoswatSurroundingsProtocol` objects that are considered for a scenario analysis.

        Returns:
            list[KoswatSurroundingsProtocol]: Collection of surroundings to include in analysis.
        """
        _surroundings = {
            _prop: _value
            for _prop, _value in self.__dict__.items()
            if isinstance(_value, KoswatSurroundingsProtocol)
        }

        def exclude_surrounding(property_name: str):
            _surroundings.pop(property_name + "_polderside", None)
            _surroundings.pop(property_name + "_dikeside", None)

        if not self.apply_buildings:
            exclude_surrounding("buildings")

        if not self.apply_railways:
            exclude_surrounding("railways")

        if not self.apply_waters:
            exclude_surrounding("waters")

        return list(_surroundings.values())

    @property
    def obstacle_locations(self) -> list[PointSurroundings]:
        """
        Overlay of locations of the different `ObstacleSurroundings` that are present.
        Buildings need to be present as input (leading for location coordinates).
        Each location represents 1 meter in a real scale map.

        Returns:
            list[PointSurroundings]: List of locations with only the closest distance to obstacle(s).
        """

        _surroundings_obstacles = list(
            filter(
                lambda x: isinstance(x, SurroundingsObstacle),
                self.surroundings_collection,
            )
        )

        def ps_sorting_key(ps_to_sort: PointSurroundings) -> int:
            return ps_to_sort.__hash__()

        _ps_keyfunc = ps_sorting_key
        _point_surroundings = sorted(
            chain(*list(map(lambda x: x.points, _surroundings_obstacles))),
            key=_ps_keyfunc,
        )
        _obstacle_locations = []
        for _, _matches in groupby(_point_surroundings, key=_ps_keyfunc):
            _lmatches = list(_matches)
            if not any(_lmatches):
                continue
            _ps_copy = _lmatches[0]
            _ps_copy.surroundings_matrix = {}
            _obstacle_locations.append(_ps_copy)
            for _matched_ps in _lmatches:
                if math.isnan(_matched_ps.closest_surrounding):
                    continue
                _ps_copy.surroundings_matrix[_matched_ps.closest_surrounding] = 1
        return _obstacle_locations

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

        return list(
            _ol.location
            for _ol in filter(_is_at_safe_distance, self.obstacle_locations)
        )
