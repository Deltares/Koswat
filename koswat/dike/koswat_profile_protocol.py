from typing import List, Optional, Protocol

from shapely.geometry.point import Point
from typing_extensions import runtime_checkable

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapper
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@runtime_checkable
class KoswatProfileProtocol(Protocol):
    input_data: KoswatInputProfileBase
    characteristic_points: CharacteristicPoints
    layers_wrapper: KoswatLayersWrapper
    location: Optional[Point]
    points: List[Point]
    profile_width: float
