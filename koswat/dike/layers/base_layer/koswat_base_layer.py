from shapely.geometry import LineString, Polygon

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterialType
from koswat.geometries.calc_library import get_polygon_coordinates


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
            material=self.material_type.name.lower(),
            geometry=_geometry,
        )
