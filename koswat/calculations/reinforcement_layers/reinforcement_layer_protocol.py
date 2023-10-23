from typing import Protocol, runtime_checkable

from shapely.geometry import LineString, MultiPolygon, Polygon

from koswat.dike.layers import KoswatLayerProtocol


@runtime_checkable
class ReinforcementLayerProtocol(KoswatLayerProtocol, Protocol):
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon
