from __future__ import annotations

from typing import List

from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


class KoswatLayers:
    base_layer: KoswatBaseLayer
    coating_layers: List[KoswatCoatingLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    @property
    def _layers(self) -> List[KoswatLayerProtocol]:
        _layers = []
        if self.base_layer:
            _layers.append(self.base_layer)
        _layers.extend(self.coating_layers)
        return _layers

    def as_data_dict(self) -> dict:
        return dict(
            base_layer=self.base_layer.as_data_dict(),
            coating_layers=[c_l.as_data_dict() for c_l in self.coating_layers],
        )
