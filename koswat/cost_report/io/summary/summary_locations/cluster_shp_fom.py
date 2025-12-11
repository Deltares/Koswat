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

from dataclasses import dataclass
from typing import Optional

from shapely import LineString, Point

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class ClusterShpFom:
    locations: list[StrategyLocationReinforcement]
    reinforced_profile: ReinforcementProfileProtocol
    left_neighbour_extent: Optional[Point] = None
    right_neighbour_extent: Optional[Point] = None

    @property
    def points_with_neighbour_extent(self) -> list[Point]:
        """
        The locations including points halfway to the left and right neighbour locations,
        if available.

        Returns:
            list[Point]: List of points with extent halfway to neighbours included.
        """
        _points = [_l.location.location for _l in self.locations]
        if self.left_neighbour_extent:
            _points.insert(0, self.left_neighbour_extent)
        if self.right_neighbour_extent:
            _points.append(self.right_neighbour_extent)
        return _points

    @property
    def old_polderside_width(self) -> float:
        """
        The original polderside width.
        """
        return self.reinforced_profile.old_profile.polderside_width

    @property
    def new_polderside_width(self) -> float:
        """
        The new polderside width.
        """
        return self.reinforced_profile.polderside_width

    @property
    def base_geometry(self) -> LineString:
        """
        The resulting geometry of all `locations` excluding the
        profile's width.

        Returns:
            LineString: Geometry representing the cluster coordinates.
        """
        return LineString(_l for _l in self.points_with_neighbour_extent)

    def get_buffered_geometry(self, width: float) -> LineString:
        """
        The `base_geometry` with an applied buffer (`width`) that
        represents the polderside's width.

        Args:
            width (float): Profile's polderside width.

        Returns:
            LineString: Resulting `base_geometry` with a buffer.
        """
        return self.base_geometry.buffer(-width, cap_style=2, single_sided=True)

    @staticmethod
    def add_neighbour_extent(
        left_cluster: "ClusterShpFom", right_cluster: "ClusterShpFom"
    ) -> None:
        """
        Adds the left and right neighbour locations to the given clusters.

        Args:
            left_cluster (ClusterShpFom): The left cluster to add the right neighbour to.
            right_cluster (ClusterShpFom): The right cluster to add the left neighbour to.
        """

        def interpolate_points(point_a: Point, point_b: Point) -> Point:
            _x = (point_a.x + point_b.x) / 2
            _y = (point_a.y + point_b.y) / 2
            return Point(_x, _y)

        left_cluster.right_neighbour_extent = interpolate_points(
            left_cluster.locations[-1].location.location,
            right_cluster.locations[0].location.location,
        )
        right_cluster.left_neighbour_extent = interpolate_points(
            left_cluster.locations[-1].location.location,
            right_cluster.locations[0].location.location,
        )
