from typing import List, Optional


class KoswatMaterial:
    name: str


class KoswatLayer:
    material: KoswatMaterial
    depth: Optional[float]


class KoswatLayers:
    base_layer: KoswatLayer
    coating_layers: List[KoswatLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []
