from shapely import geometry

from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol
from koswat.dike.material.koswat_material import KoswatMaterialFactory


class KoswatBaseLayerBuilder(KoswatLayerBuilderProtocol):
    layer_data: dict
    upper_linestring: geometry.LineString

    def __init__(self) -> None:
        self.layer_data = {}
        self.upper_linestring = None

    def build(self) -> KoswatBaseLayer:
        if not self.upper_linestring:
            raise ValueError("Profile line geometry needs to be provided.")
        _material_data = self.layer_data.get("material", None)
        if not _material_data:
            raise ValueError("Material data needs to be provided.")
        _material = KoswatMaterialFactory.get_material(self.layer_data["material"])
        _layer = KoswatBaseLayer()
        _geometry_points = []
        _upper_layer_points = list(self.upper_linestring.coords)
        _geometry_points.extend(_upper_layer_points)
        _geometry_points.append(_upper_layer_points[0])
        _layer.geometry = geometry.Polygon(_geometry_points)
        _layer.material = _material
        _layer.upper_points = self.upper_linestring
        return _layer
