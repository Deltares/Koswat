from typing import List, Optional, Protocol

from shapely.geometry.point import Point
from typing_extensions import runtime_checkable

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.layers.koswat_layers import KoswatLayers
from koswat.dike.profile.koswat_input_profile import KoswatInputProfile


@runtime_checkable
class KoswatProfileProtocol(Protocol):
    input_data: KoswatInputProfile
    characteristic_points: CharacteristicPoints
    layers: KoswatLayers
    location: Optional[Point]
    points: List[Point]
    profile_width: float
