from typing import List, Protocol

from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


class KoswatLayersWrapperProtocol(Protocol):
    base_layer: KoswatBaseLayer
    coating_layers: List[KoswatCoatingLayer]
    layers: List[KoswatLayerProtocol]

    def as_data_dict(self) -> dict:
        """
        Returns the layers as a dictionary.

        Returns:
            dict: Dictionary containing all the information of the wrapper layers (`KoswatLayerProtocol`).
        """
        pass
