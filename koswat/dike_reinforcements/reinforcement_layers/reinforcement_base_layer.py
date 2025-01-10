from __future__ import annotations

from shapely.geometry import LineString, MultiPolygon, Polygon

from koswat.core.geometries.calc_library import get_polygon_coordinates
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


class ReinforcementBaseLayer(ReinforcementLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None
        self.new_layer_geometry = None

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type.name,
            geometry=_geometry,
        )

    @classmethod
    def from_koswat_base_layer(
        cls, base_layer: KoswatBaseLayer
    ) -> ReinforcementBaseLayer:
        _reinforced_base_layer = cls()
        _reinforced_base_layer.__dict__ = base_layer.__dict__
        return _reinforced_base_layer
