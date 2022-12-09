import math

from shapely.geometry import LineString, Polygon

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterial
from koswat.geometries.calc_library import get_polygon_coordinates


class KoswatCoatingLayer(KoswatLayerProtocol):
    depth: float
    lower_linestring: LineString
    upper_points: LineString
    material: KoswatMaterial
    outer_geometry: Polygon
    material_geometry: Polygon

    def __init__(self) -> None:
        self.material = None
        self.outer_geometry = None
        self.lower_linestring = None
        self.upper_points = None
        self.material_geometry = None
        self.depth = math.nan

    def get_coated_geometry(self) -> Polygon:
        if not self.material_geometry or not self.outer_geometry:
            return None
        return self.outer_geometry.difference(self.material_geometry)

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material.name,
            depth=self.depth,
            geometry=_geometry,
        )
