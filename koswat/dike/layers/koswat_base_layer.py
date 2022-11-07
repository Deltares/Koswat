from shapely.geometry import LineString, Polygon

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterial


class KoswatBaseLayer(KoswatLayerProtocol):
    material: KoswatMaterial
    upper_points: LineString
    geometry: Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None
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
        return dict(material=self.material.name)