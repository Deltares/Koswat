from __future__ import annotations

from shapely.geometry import LineString, MultiPolygon, Polygon

from koswat.calculations.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)
from koswat.core.geometries.calc_library import get_polygon_coordinates
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class ReinforcementCoatingLayer(ReinforcementLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    old_layer_geometry: Polygon
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    removal_layer_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None
        self.new_layer_geometry = None
        self.removal_layer_geometry = None

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type.name,
            depth=self.depth,
            geometry=_geometry,
        )

    @classmethod
    def from_koswat_coating_layer(
        cls, coating_layer: KoswatCoatingLayer
    ) -> ReinforcementCoatingLayer:
        _reinforced_coating_layer = cls()
        _reinforced_coating_layer.__dict__ = coating_layer.__dict__
        return _reinforced_coating_layer

    @classmethod
    def with_same_outer_geometry(
        cls, coating_layer: KoswatCoatingLayer
    ) -> ReinforcementCoatingLayer:
        """
        Creates a new reinforcement coating layer which does not differ
        in geometry from the provided coating layer. This was found to
        be needed in KOSWAT_82.

        Args:
            coating_layer (KoswatCoatingLayer): Base coating layer.

        Returns:
            ReinforcementCoatingLayer: Resulting coating layer with "empty"
            polygons for added / removed (layer) geometries.
        """
        _reinforced_coating_layer = cls.from_koswat_coating_layer(coating_layer)
        _reinforced_coating_layer.old_layer_geometry = coating_layer.outer_geometry
        _reinforced_coating_layer.removal_layer_geometry = Polygon()
        _reinforced_coating_layer.new_layer_geometry = Polygon()
        _reinforced_coating_layer.new_layer_surface = LineString()
        return _reinforced_coating_layer
