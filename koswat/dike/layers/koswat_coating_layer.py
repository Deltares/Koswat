import math

from shapely.geometry import LineString, Polygon

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterial


class KoswatCoatingLayer(KoswatLayerProtocol):
    depth: float
    layer_points: LineString
    upper_points: LineString
    material: KoswatMaterial
    geometry: Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None
        self.layer_points = None
        self.upper_points = None
        self.depth = math.nan

    def as_data_dict(self) -> dict:
        return dict(material=self.material.name, depth=self.depth)
