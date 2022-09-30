from __future__ import annotations

import math
from typing import List

from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_material import KoswatMaterial, KoswatMaterialFactory


class KoswatLayer:
    material: KoswatMaterial
    geometry: Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None


class KoswatLayers:
    base_layer: KoswatLayer
    coating_layers: List[KoswatLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []
