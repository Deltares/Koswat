import copy
import math
from dataclasses import dataclass, field
from itertools import chain, groupby

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)


@dataclass
class ObstacleSurroundingsWrapper(BaseSurroundingsWrapper):
    apply_waterside: bool = False
    apply_buildings: bool = False
    apply_railways: bool = False
    apply_waters: bool = False
    apply_infrastructure: bool = True

    reinforcement_min_separation: float = math.nan
    reinforcement_min_buffer: float = math.nan

    # Polderside
    buildings_polderside: SurroundingsObstacle = field(
        default_factory=SurroundingsObstacle
    )
    railways_polderside: SurroundingsObstacle = field(
        default_factory=SurroundingsObstacle
    )
    waters_polderside: SurroundingsObstacle = field(
        default_factory=SurroundingsObstacle
    )

    # Dikeside (not yet supported)
    buildings_dikeside: SurroundingsObstacle = None
    railways_dikeside: SurroundingsObstacle = None
    waters_dikeside: SurroundingsObstacle = None

    def _exclude_surroundings(self, surroundings_dict: dict) -> dict:
        def exclude_surrounding(property_name: str):
            surroundings_dict.pop(property_name + "_polderside", None)
            surroundings_dict.pop(property_name + "_dikeside", None)

        if not self.apply_buildings:
            exclude_surrounding("buildings")

        if not self.apply_railways:
            exclude_surrounding("railways")

        if not self.apply_waters:
            exclude_surrounding("waters")
        return surroundings_dict

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
                self.surroundings_collection.values(),
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
            _ps_copy = copy.deepcopy(_lmatches[0])
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
