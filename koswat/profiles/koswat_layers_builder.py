from __future__ import annotations

import math
from typing import List

from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_layers import KoswatLayer, KoswatLayers
from koswat.profiles.koswat_material import KoswatMaterialFactory


class KoswatLayersBuilder:
    layers_data: dict = {}
    profile_points: List[Point] = []

    def _build_layer(self, parent_geometry: Polygon, layer_data: dict) -> KoswatLayer:
        _layer = KoswatLayer()
        _layer.depth = layer_data.get("depth", math.nan)
        if math.isnan(_layer.depth):
            # Usually only for the base layer (sand)
            _layer.geometry = parent_geometry
        # else:
        # TODO
        # _layer.geometry = ??
        _layer.material = KoswatMaterialFactory.get_material(layer_data["material"])
        return _layer

    def _get_profile_polygon(self, profile_points: List[Point]) -> Polygon:
        _geometry_points = []
        _geometry_points.extend(profile_points)
        # Close polygon
        _geometry_points.append(profile_points[0])
        return Polygon(_geometry_points)

    def build(self) -> KoswatLayers:
        _onion_geometry = self._get_profile_polygon(self.profile_points)
        _koswat_layers = KoswatLayers()
        _koswat_layers.coating_layers = []
        for c_layer_data in self.layers_data.get("coating_layers", []):
            _c_layer = self._build_layer(_onion_geometry, c_layer_data)
            _onion_geometry -= _c_layer
            _koswat_layers.coating_layers.append(_c_layer)
        _koswat_layers.base_layer = self._build_layer(
            _onion_geometry, self.layers_data["base_layer"]
        )
        return _koswat_layers

    @staticmethod
    def layers_as_dict(layers: KoswatLayers) -> dict:
        _base_layer = dict(material=layers.base_layer.material.name, depth=math.nan)
        # TODO: Logic for coating layers.
        return dict(base_layer=_base_layer, coating_layers=dict())
