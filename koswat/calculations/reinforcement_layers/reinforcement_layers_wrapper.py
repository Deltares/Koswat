from koswat.calculations.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)
from koswat.calculations.reinforcement_layers.reinforcement_base_layer import (
    ReinforcementBaseLayer,
)
from koswat.calculations.reinforcement_layers.reinforcement_coating_layer import (
    ReinforcementCoatingLayer,
)
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class ReinforcementLayersWrapper(KoswatLayersWrapperProtocol):
    base_layer: ReinforcementBaseLayer
    coating_layers: list[ReinforcementCoatingLayer]

    def __init__(self) -> None:
        self.base_layer = None
        self.coating_layers = []

    def as_data_dict(self) -> dict:
        return dict(
            base_layer=self.base_layer.as_data_dict(),
            coating_layers=[c_l.as_data_dict() for c_l in self.coating_layers],
        )

    def get_layer(self, material_type: KoswatMaterialType) -> ReinforcementCoatingLayer:
        _found_layer = next(
            (
                _layer
                for _layer in self.coating_layers
                if _layer.material_type == material_type
            ),
            None,
        )
        if not _found_layer:
            raise ValueError(
                "Material {} not present in the layers.".format(material_type.name)
            )
        return _found_layer

    @property
    def layers(self) -> list[ReinforcementLayerProtocol]:
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
