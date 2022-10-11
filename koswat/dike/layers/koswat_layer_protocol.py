from typing import Protocol

from shapely import geometry
from typing_extensions import runtime_checkable

from koswat.dike.material.koswat_material import KoswatMaterial


@runtime_checkable
class KoswatLayerProtocol(Protocol):
    material: KoswatMaterial
    geometry: geometry.Polygon

    def as_data_dict(self) -> dict:
        pass
