from typing import List, Optional, Protocol, runtime_checkable

from shapely.geometry.point import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper


@runtime_checkable
class KoswatProfileProtocol(Protocol):
    input_data: KoswatInputProfileProtocol
    characteristic_points: CharacteristicPoints
    layers_wrapper: KoswatLayersWrapper
    location: Optional[Point]
    points: List[Point]
    profile_width: float
