from typing import Protocol

from shapely import geometry
from typing_extensions import runtime_checkable

from koswat.dike.material.koswat_material_type import KoswatMaterialType


@runtime_checkable
class KoswatLayerProtocol(Protocol):
    material_type: KoswatMaterialType
    layer_points: geometry.LineString
    upper_points: geometry.LineString
    outer_geometry: geometry.Polygon
    material_geometry: geometry.Polygon

    def as_data_dict(self) -> dict:
        pass
