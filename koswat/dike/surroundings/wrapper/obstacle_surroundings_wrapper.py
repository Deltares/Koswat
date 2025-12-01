"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
import math
from dataclasses import dataclass, field
from itertools import chain, groupby

from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)


@dataclass
class ObstacleSurroundingsWrapper(BaseSurroundingsWrapper):
    reinforcement_min_separation: float = math.nan
    reinforcement_min_buffer: float = math.nan

    buildings: SurroundingsObstacle = field(default_factory=SurroundingsObstacle)
    railways: SurroundingsObstacle = field(default_factory=SurroundingsObstacle)
    waters: SurroundingsObstacle = field(default_factory=SurroundingsObstacle)
    custom_obstacles: SurroundingsObstacle = field(default_factory=SurroundingsObstacle)

    @property
    def obstacle_locations(self) -> list[PointObstacleSurroundings]:
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
                [self.buildings, self.railways, self.waters, self.custom_obstacles],
            )
        )

        def ps_sorting_key(ps_to_sort: PointObstacleSurroundings) -> int:
            return ps_to_sort.__hash__()

        _ps_keyfunc = ps_sorting_key
        _point_obstacle_surroundings = sorted(
            chain(*list(map(lambda x: x.points, _surroundings_obstacles))),
            key=_ps_keyfunc,
        )
        _obstacle_locations = []
        for _, _matches in groupby(_point_obstacle_surroundings, key=_ps_keyfunc):
            _lmatches = list(_matches)
            if not any(_lmatches):
                continue
            _ps_copy = copy.deepcopy(_lmatches[0])
            for _matched_ps in _lmatches[1:]:
                if math.isnan(_matched_ps.closest_obstacle):
                    continue
                _ps_copy.merge(_matched_ps)
            _obstacle_locations.append(_ps_copy)
        return _obstacle_locations

    def get_locations_at_safe_distance(
        self, distance: float
    ) -> list[PointSurroundings]:
        """
        Gets all locations which are safe from obstacle surroundings in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            list[PointSurroundings]: List of safe locations (points with surroundings).
        """

        def _is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if math.isnan(point_surroundings.closest_obstacle):
                return True
            return distance < point_surroundings.closest_obstacle

        return list(filter(_is_at_safe_distance, self.obstacle_locations))
