from __future__ import annotations

from typing import List

from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside


class KoswatProfile:

    input_data: KoswatInputProfile
    waterside: Waterside
    polderside: Polderside
    layers: KoswatLayers

    def __init__(self) -> None:
        self.input_data = None
        self.waterside = Waterside()
        self.polderside = Polderside()
        self.layers = None

    @property
    def points(self) -> List[Point]:
        """
        The combination of points from both water and polder sides.

        Returns:
            List[Point]: A total of eight points comforming the `KoswatProfile`.
        """
        _points = []
        _points.extend(self.waterside.points)
        _points.extend(self.polderside.points)
        return _points
