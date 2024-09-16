import math
from dataclasses import dataclass, field
from itertools import chain, groupby

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


@dataclass
class SurroundingsWrapper:
    dike_section: str = ""
    traject: str = ""
    subtraject: str = ""

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
                if math.isnan(_matched_ps.closest_obstacle):
                    continue
                _ps_copy.surroundings_matrix[_matched_ps.closest_obstacle] = 1
        return _obstacle_locations

    def get_locations_at_safe_distance(
        self, distance: float
    ) -> list[PointSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[PointSurroundings]: List of safe locations (points with surroundings).
        """

        def _is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if math.isnan(point_surroundings.closest_obstacle):
                return True
            return distance < point_surroundings.closest_obstacle

        return list(filter(_is_at_safe_distance, self.obstacle_locations))
