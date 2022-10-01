from __future__ import annotations

import math
from typing import List

from shapely import geometry

from koswat.profiles.koswat_layers import (
    KoswatBaseLayer,
    KoswatCoatingLayer,
    KoswatLayerProtocol,
    KoswatLayers,
)
from koswat.profiles.koswat_material import KoswatMaterialFactory


class KoswatLayersBuilder:
    layers_data: dict = {}
    profile_points: List[geometry.Point] = []

    def _build_base_layer(
        self, upper_layer_linestring: geometry.LineString, layer_data: dict
    ) -> KoswatBaseLayer:
        _material = KoswatMaterialFactory.get_material(layer_data["material"])
        _layer = KoswatBaseLayer()
        _geometry_points = []
        _upper_layer_points = list(upper_layer_linestring.coords)
        _geometry_points.extend(_upper_layer_points)
        _geometry_points.append(_upper_layer_points[0])
        _layer.geometry = geometry.Polygon(_geometry_points)
        _layer.material = _material
        return _layer

    def _build_coating_layer(
        self, upper_layer_points: geometry.LineString, layer_data: dict
    ) -> KoswatCoatingLayer:
        _depth = layer_data.get("depth", math.nan)
        _material = KoswatMaterialFactory.get_material(layer_data["material"])
        if math.isnan(_depth):
            # Usually only for the base layer (sand)
            raise ValueError(
                f"Depth cannot be negative in a coating layer. Layer: {_material.name}"
            )

        # Get the offset linestring
        _offset_geom_linestring = upper_layer_points.parallel_offset(
            -_layer.depth, side="left", join_style=2
        )
        _offset_geom_coords = list(_offset_geom_linestring.coords)
        # Reverse it so it can be built into a polygon with the upper layer.
        _offset_geom_coords.reverse()
        _offset_geom_coords.append(upper_layer_points[0])
        _offset_geom_coords.insert(0, upper_layer_points[-1])
        # Create the new coating layer
        _layer = KoswatCoatingLayer()
        _layer_points = list(upper_layer_points.coords).extend(_offset_geom_coords)
        _layer.layer_points = _layer_points
        _layer.geometry = geometry.Polygon(_layer_points)
        _layer.material = _material

        return _layer

    def build(self) -> KoswatLayers:
        _koswat_layers = KoswatLayers()
        _koswat_layers.coating_layers = []
        _parent_points = geometry.LineString(self.profile_points)
        for c_layer_data in self.layers_data.get("coating_layers", []):
            _c_layer = self._build_coating_layer(_parent_points, c_layer_data)
            _parent_points = _c_layer.layer_points
            _koswat_layers.coating_layers.append(_c_layer)
        _koswat_layers.base_layer = self._build_base_layer(
            _parent_points, self.layers_data["base_layer"]
        )
        return _koswat_layers

    @staticmethod
    def layers_as_dict(layers: KoswatLayers) -> dict:
        _base_layer = dict(material=layers.base_layer.material.name, depth=math.nan)
        # TODO: Logic for coating layers.
        return dict(base_layer=_base_layer, coating_layers=dict())
