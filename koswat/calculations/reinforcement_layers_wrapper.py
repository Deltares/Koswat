from __future__ import annotations

from typing import List, Protocol

from shapely.geometry import LineString, Polygon

from koswat.dike.layers import KoswatLayerProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.material.koswat_material import KoswatMaterialType
from koswat.geometries.calc_library import get_polygon_coordinates


class ReinforcementLayerProtocol(KoswatLayerProtocol, Protocol):
    new_layer_geometry: Polygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon


class ReinforcementCoatingLayer(KoswatLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    old_layer_geometry: Polygon
    new_layer_geometry: Polygon
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


class ReinforcementBaseLayer(ReinforcementLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    new_layer_geometry: Polygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None
        self.new_layer_geometry = None

    @property
    def layer_points(self) -> LineString:
        """
        A Koswat Base Layer has no layer points, only upper surface.

        Returns:
            None: Only upper (coating layer) points available.
        """
        return None

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


class ReinforcementLayersWrapper(KoswatLayersWrapperProtocol):
    base_layer: ReinforcementBaseLayer
    coating_layers: List[ReinforcementCoatingLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    def as_data_dict(self) -> dict:
        return dict(
            base_layer=self.base_layer.as_data_dict(),
            coating_layers=[c_l.as_data_dict() for c_l in self.coating_layers],
        )

    def get_layer(self, material: str) -> ReinforcementCoatingLayer:
        _found_layer = next(
            (
                _layer
                for _layer in self.coating_layers
                if _layer.material_type.name.lower() == material.lower()
            ),
            None,
        )
        if not _found_layer:
            raise ValueError("Material {} not present in the layers.".format(material))
        return _found_layer

    @property
    def layers(self) -> List[ReinforcementLayerProtocol]:
        """
        All the stored layers being the `KoswatBaseLayer` the latest one in the collection.

        Returns:
            List[KoswatLayerProtocol]: Ordered list of `KoswatLayerProtocol`.
        """
        _layers = []
        _layers.extend(self.coating_layers)
        if self.base_layer:
            _layers.append(self.base_layer)
        return _layers
