from __future__ import annotations

import math
from typing import List, Protocol

from shapely import geometry
from typing_extensions import runtime_checkable

from koswat.profiles.koswat_material import KoswatMaterial


@runtime_checkable
class KoswatLayerProtocol(Protocol):
    material: KoswatMaterial
    geometry: geometry.Polygon

    def as_data_dict(self) -> dict:
        pass


class KoswatBaseLayer(KoswatLayerProtocol):
    material: KoswatMaterial
    geometry: geometry.Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None

    def as_data_dict(self) -> dict:
        return dict(material=self.material.name)


class KoswatCoatingLayer(KoswatLayerProtocol):
    depth: float
    layer_points: geometry.LineString
    material: KoswatMaterial
    geometry: geometry.Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None
        self.depth = math.nan

    def as_data_dict(self) -> dict:
        return dict(material=self.material.name, depth=self.depth)


class KoswatLayers:
    base_layer: KoswatBaseLayer
    coating_layers: List[KoswatCoatingLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    @property
    def _layers(self) -> List[KoswatLayerProtocol]:
        _layers = []
        _layers.append(self.base_layer)
        _layers.extend(self.coating_layers)
        return _layers

    def as_data_dict(self) -> dict:
        return dict(
            base_layer=self.base_layer.as_data_dict(),
            coating_layers=[c_l.as_data_dict() for c_l in self.coating_layers],
        )
