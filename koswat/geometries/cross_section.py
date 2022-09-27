from typing import List, Optional, Protocol


class KoswatGeometry(Protocol):
    pass

class Layer(KoswatGeometry):
    pass

class CrossSection(KoswatGeometry):
    base_layer: Layer
    layers: Optional[List[Layer]]
    pass
