from typing import List, Protocol

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapperProtocol


class ReinforcementLayerProtocol(KoswatLayerProtocol, Protocol):
    pass

class ReinforcementCoatingLayer(KoswatLayerProtocol):
    pass

class ReinforcementBaseLayer(ReinforcementLayerProtocol):
    pass

class ReinforcementLayersWrapper(KoswatLayersWrapperProtocol):
    base_layer: ReinforcementBaseLayer
    coating_layers: List[ReinforcementCoatingLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    @property
    def layers(self) -> List[ReinforcementLayerProtocol]:
        """
        All the stored layers being the `KoswatBaseLayer` the latest one in the collection.

        Returns:
            List[KoswatLayerProtocol]: Ordered list of `KoswatLayerProtocol`.
        """
        _layers = []
        _layers.extend(self.coating_layers)
        if self.base_layer:
            _layers.append(self.base_layer)
        return _layers