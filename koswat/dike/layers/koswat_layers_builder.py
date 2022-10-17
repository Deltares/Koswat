from __future__ import annotations

import math
from typing import List

from shapely import geometry

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_layers import (
    KoswatBaseLayer,
    KoswatCoatingLayer,
    KoswatLayers,
)
from koswat.dike.material.koswat_material import KoswatMaterialFactory


class KoswatLayersBuilder(BuilderProtocol):
    layers_data: dict = {}
    profile_points: List[geometry.Point] = []
    profile_geometry: geometry.Polygon = None

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
        _layer.upper_points = upper_layer_linestring
        return _layer

    def _build_coating_layer(
        self, upper_layer_linestring: geometry.LineString, layer_data: dict
    ) -> KoswatCoatingLayer:
        _depth = layer_data.get("depth", math.nan)
        _material = KoswatMaterialFactory.get_material(layer_data["material"])
        _base_geometry = self._get_profile_geometry()
        if math.isnan(_depth):
            # Usually only for the base layer (sand)
            raise ValueError(
                f"Depth cannot be negative in a coating layer. Layer: {_material.name}"
            )

        # Get the offset linestring
        _offset_geom_linestring = upper_layer_linestring.parallel_offset(
            -_depth, side="left", join_style=2
        )
        # We need to cut the 'y' axis as it might have gone below
        _offset_geom_linestring = _offset_geom_linestring.intersection(_base_geometry)
        _offset_geom_coords = list(_offset_geom_linestring.coords)
        if _offset_geom_coords[-1][0] > _offset_geom_coords[0][0]:
            # Reverse it so it can be built into a polygon with the upper layer.
            _offset_geom_coords.reverse()
        # Avoid duplicates while preserving order
        _layer_geometry_points = list(dict.fromkeys(upper_layer_linestring.coords))
        _layer_geometry_points.extend(_offset_geom_coords)
        _layer_geometry_points.append(_layer_geometry_points[0])
        _offset_geom_coords.reverse()

        # Create the new coating layer
        _layer = KoswatCoatingLayer()
        _layer.upper_points = upper_layer_linestring
        _layer.layer_points = geometry.LineString(_offset_geom_coords)
        _layer.geometry = geometry.Polygon(_layer_geometry_points)
        _layer.material = _material
        _layer.depth = _depth
        return _layer

    def _get_profile_geometry(self) -> geometry.Polygon:
        _geometry_points = []
        _geometry_points.extend(self.profile_points)
        _geometry_points.append(self.profile_points[0])
        return geometry.Polygon(_geometry_points)

    def build(self) -> KoswatLayers:
        _koswat_layers = KoswatLayers()
        _koswat_layers.coating_layers = []
        _surface_coating_layer = geometry.LineString(self.profile_points)
        for c_layer_data in self.layers_data.get("coating_layers", []):
            _c_layer = self._build_coating_layer(_surface_coating_layer, c_layer_data)
            _surface_coating_layer = _c_layer.layer_points
            _koswat_layers.coating_layers.append(_c_layer)
        _koswat_layers.base_layer = self._build_base_layer(
            _surface_coating_layer, self.layers_data["base_layer"]
        )
        return _koswat_layers

    @staticmethod
    def layers_as_dict(layers: KoswatLayers) -> dict:
        _base_layer = dict(material=layers.base_layer.material.name, depth=math.nan)
        # TODO: Logic for coating layers.
        return dict(base_layer=_base_layer, coating_layers=dict())
