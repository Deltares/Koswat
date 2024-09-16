from __future__ import annotations

import math
from dataclasses import dataclass

from shapely.geometry.point import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class KoswatProfileBase(KoswatProfileProtocol):
    """
    Basic definition and implementation of a `KoswatProfileProtocol`. It represents the initial koswat profile being provided by the user from which further calculations will be made.
    """

    input_data: KoswatInputProfileBase = None
    characteristic_points: CharacteristicPoints = None
    layers_wrapper: KoswatLayersWrapper = None
    location: Point | None = None

    @property
    def points(self) -> list[Point]:
        """
        The combination of points from both water and polder sides.

        Returns:
            list[Point]: A total of eight points comforming the `KoswatProfile`.
        """
        if not self.characteristic_points:
            return []
        return self.characteristic_points.points

    @property
    def profile_width(self) -> float:
        """
        The profile extent from the lowest (left-most) x-coordinate to the largest (right-most) x-coordinate from a dike geometry polygon.

        Returns:
            float: Total distance.
        """
        if not self.points:
            return math.nan

        # This assumes coordinates are ordered based on the 'x' coordinate
        # as they come from our `CharacteristicPoints.points` property method.

        return self.points[-1].x - self.points[0].x

    @property
    def profile_height(self) -> float:
        """
        The profile highest point (largest y-coordinate).

        Returns:
            float: Greatest y-coordinate.
        """
        if not self.points:
            return math.nan
        return max(_p.y for _p in self.points if _p)
