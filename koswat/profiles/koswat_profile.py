from __future__ import annotations

from typing import List

from shapely.geometry.point import Point

from koswat.profiles.characteristic_points import CharacteristicPoints
from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers


class KoswatProfile:

    input_data: KoswatInputProfile
    characteristic_points: CharacteristicPoints
    layers: KoswatLayers

    def __init__(self) -> None:
        self.input_data = None
        self.layers = None
        self.characteristic_points = None

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
