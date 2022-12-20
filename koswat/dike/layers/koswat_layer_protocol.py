from typing import Protocol, runtime_checkable

from shapely import geometry

from koswat.dike.material.koswat_material_type import KoswatMaterialType


@runtime_checkable
class KoswatLayerProtocol(Protocol):
    material_type: KoswatMaterialType
    layer_points: geometry.LineString
    upper_points: geometry.LineString
    outer_geometry: geometry.Polygon
    material_geometry: geometry.Polygon

    def as_data_dict(self) -> dict:
        """
        Returns the information related to an instance of the `KoswatLayerProtocol`.

        Returns:
            dict: custom dictionary with the relevant data.
        """
        pass
