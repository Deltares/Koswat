from typing import Protocol, runtime_checkable
from koswat.dike.layers import KoswatLayerProtocol
from shapely.geometry import LineString, Polygon, MultiPolygon


@runtime_checkable
class ReinforcementLayerProtocol(KoswatLayerProtocol, Protocol):
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon
