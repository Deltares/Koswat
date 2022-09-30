from __future__ import annotations

import math
from typing import List

from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_material import KoswatMaterial, KoswatMaterialFactory


class KoswatLayer:
    material: KoswatMaterial = None
    geometry: Polygon = None

    @classmethod
    def from_dict(cls, data_dict: dict) -> KoswatLayer:
        _layer = cls()
        _layer.material = KoswatMaterialFactory.get_material(data_dict["material"])
        _layer.geometry = data_dict.get("geometry", math.nan)
        return _layer


class KoswatLayers:
    base_layer: KoswatLayer
    coating_layers: List[KoswatLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    @classmethod
    def from_dict(cls, data_dict: dict) -> KoswatLayers:
        _layers = KoswatLayers()
        _layers.base_layer = KoswatLayer.from_dict(data_dict["base_layer"])
        _layers.coating_layers = list(
            map(KoswatLayer.from_dict, data_dict.get("coating_layers", []))
        )
        return _layers
