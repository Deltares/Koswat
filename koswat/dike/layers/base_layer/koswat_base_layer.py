from shapely.geometry import LineString, Polygon

from koswat.core.geometries.calc_library import get_polygon_coordinates
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class KoswatBaseLayer(KoswatLayerProtocol):
    material_type: KoswatMaterialType
    upper_points: LineString
    outer_geometry: Polygon
    material_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type,
            geometry=_geometry,
        )
