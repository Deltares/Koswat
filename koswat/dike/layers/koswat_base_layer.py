from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material import KoswatMaterial


class KoswatBaseLayer(KoswatLayerProtocol):
    material: KoswatMaterial
    geometry: geometry.Polygon

    def __init__(self) -> None:
        self.material = None
        self.geometry = None

    def as_data_dict(self) -> dict:
        return dict(material=self.material.name)
