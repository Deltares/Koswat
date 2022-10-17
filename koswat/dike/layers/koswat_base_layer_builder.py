from shapely import geometry

from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol
from koswat.dike.material.koswat_material import KoswatMaterialFactory


class KoswatBaseLayerBuilder(KoswatLayerBuilderProtocol):
    layer_data: dict
    upper_linestring: geometry.LineString

    def build(self) -> KoswatBaseLayer:
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
