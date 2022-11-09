from typing import List

from shapely.geometry import Point, Polygon

from koswat.calculations.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.layers.koswat_layers_wrapper_builder import (
    KoswatLayersWrapperBuilderProtocol,
)


class StandardReinforcementLayersWrapperBuilder(KoswatLayersWrapperBuilderProtocol):
    layers_data: dict  # Previous profile layers wrapper
    profile_points: List[Point]  # Characteristic points.

    def build(self) -> ReinforcementLayersWrapper:
        pass
