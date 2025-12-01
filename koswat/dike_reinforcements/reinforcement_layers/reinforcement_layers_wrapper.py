"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from koswat.dike.layers.layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_base_layer import (
    ReinforcementBaseLayer,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_coating_layer import (
    ReinforcementCoatingLayer,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


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
