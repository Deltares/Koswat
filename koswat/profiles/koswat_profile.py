from __future__ import annotations

from typing import List

from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers


class KoswatProfile:

    input_data: KoswatInputProfile
    layers: KoswatLayers

    def __init__(self) -> None:
        self.input_data = None
        self.layers = None

    @property
    def points(self) -> List[Point]:
        """
        The combination of points from both water and polder sides.

        Returns:
            List[Point]: A total of eight points comforming the `KoswatProfile`.
        """
        if not self.input_data or not self.input_data.characteristic_points:
            return []
        return self.input_data.characteristic_points.points
