from __future__ import annotations

import math
from typing import List

from koswat.profiles.koswat_material import KoswatMaterial, KoswatMaterialFactory


class KoswatLayer:
    material: KoswatMaterial
    depth: float

    def __init__(self) -> None:
        self.material = None
        self.depth = math.nan

    @classmethod
    def from_dict(cls, data_dict: dict) -> KoswatLayer:
        _layer = cls()
        _layer.material = KoswatMaterialFactory.get_material(data_dict["material"])
        _layer.depth = data_dict.get("depth", math.nan)
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
