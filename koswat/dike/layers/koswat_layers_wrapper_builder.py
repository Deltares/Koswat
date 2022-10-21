from __future__ import annotations

from typing import List

from shapely import geometry

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_base_layer_builder import KoswatBaseLayerBuilder
from koswat.dike.layers.koswat_coating_layer_builder import KoswatCoatingLayerBuilder
from koswat.dike.layers.koswat_layers_wrapper import (
    KoswatBaseLayer,
    KoswatCoatingLayer,
    KoswatLayersWrapper,
)


class KoswatLayersWrapperBuilder(BuilderProtocol):
    layers_data: dict
    profile_points: List[geometry.Point]
    profile_geometry: geometry.Polygon

    def __init__(self) -> None:
        self.layers_data = {}
        self.profile_points = []
        self.profile_geometry = None

    def _get_profile_geometry(self) -> geometry.Polygon:
        _geometry_points = []
        _geometry_points.extend(self.profile_points)
        _geometry_points.append(self.profile_points[0])
        return geometry.Polygon(_geometry_points)

    def _get_coating_layers(self) -> List[KoswatCoatingLayer]:
        _c_layers_data = self.layers_data.get("coating_layers", [])
        if not _c_layers_data:
            return []
        _builder = KoswatCoatingLayerBuilder()
        _builder.upper_linestring = geometry.LineString(self.profile_points)
        _builder.base_geometry = self._get_profile_geometry()
        _layers = []
        for c_layer_data in _c_layers_data:
            _builder.layer_data = c_layer_data
            _c_layer = _builder.build()
            _builder.upper_linestring = _c_layer.layer_points
            _layers.append(_c_layer)
        return _layers

    def _get_base_layer(self, upper_linestring: geometry.LineString) -> KoswatBaseLayer:
        _builder = KoswatBaseLayerBuilder()
        _builder.layer_data = self.layers_data["base_layer"]
        _builder.upper_linestring = upper_linestring
        return _builder.build()

    def build(self) -> KoswatLayersWrapper:
        _koswat_layers = KoswatLayersWrapper()
        _koswat_layers.coating_layers = self._get_coating_layers()
        _base_layer_surface = (
            _koswat_layers.coating_layers[-1].layer_points
            if any(_koswat_layers.coating_layers)
            else geometry.LineString(self.profile_points)
        )
        _koswat_layers.base_layer = self._get_base_layer(_base_layer_surface)
        return _koswat_layers
