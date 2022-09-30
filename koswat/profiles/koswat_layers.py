from __future__ import annotations

import math
from typing import List

from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_material import KoswatMaterial


class KoswatLayer:
    material: KoswatMaterial
    geometry: Polygon
    depth: float

    def __init__(self) -> None:
        self.material = None
        self.geometry = None
        self.depth = math.nan

    def as_data_dict(self) -> dict:
        return dict(material=self.material.name, depth=self.depth)


class KoswatLayers:
    base_layer: KoswatLayer
    coating_layers: List[KoswatLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    def as_data_dict(self) -> dict:
        return dict(
            base_layer=self.base_layer.as_data_dict(),
            coating_layers=[c_l.as_data_dict() for c_l in self.coating_layers],
        )
