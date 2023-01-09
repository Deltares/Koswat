from __future__ import annotations

import math
from typing import List, Optional

from shapely.geometry.point import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class KoswatProfileBase(KoswatProfileProtocol):
    """
    Basic definition and implementation of a `KoswatProfileProtocol`. It represents the initial koswat profile being provided by the user from which further calculations will be made.
    """

    input_data: KoswatInputProfileBase
    characteristic_points: CharacteristicPoints
    layers_wrapper: KoswatLayersWrapper
    location: Optional[Point]

    def __init__(self) -> None:
        self.input_data = None
        self.layers_wrapper = None
        self.characteristic_points = None
        self.location = None

    @property
    def points(self) -> List[Point]:
        """
        The combination of points from both water and polder sides.

        Returns:
            List[Point]: A total of eight points comforming the `KoswatProfile`.
        """
        if not self.characteristic_points:
            return []
        return self.characteristic_points.points

    @property
    def profile_width(self) -> float:
        """
        The profile extent from the lowest (left-most) x-coordinate to the largets (right-most) x-coordinate from a dike geometry polygon.

        Returns:
            float: Total distance.
        """
        if not self.points:
            return math.nan
        return self.points[-1].x - self.points[0].x
