import math
from typing import List

from shapely import geometry

from koswat.dike.layers.coating_layer.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol
from koswat.geometries.calc_library import remove_layer_from_polygon


class KoswatCoatingLayerBuilder(KoswatLayerBuilderProtocol):
    upper_linestring: geometry.LineString
    layer_data: dict
    base_geometry: geometry.Polygon

    def __init__(self) -> None:
        self.upper_linestring = None
        self.layer_data = None
        self.base_geometry = None

    def _get_offset_coordinates(self, depth: float) -> List[geometry.Point]:
        # Get the offset linestring
        _offset_geom_linestring = self.upper_linestring.parallel_offset(
            -depth, side="left", join_style=2, mitre_limit=10
        )
        # We need to cut the 'y' axis as it might have gone below
        _offset_geom_linestring = _offset_geom_linestring.intersection(
            self.base_geometry
        )
        _offset_geom_coords = list(_offset_geom_linestring.coords)
        if _offset_geom_coords[-1][0] > _offset_geom_coords[0][0]:
            # Reverse it so it can be built into a polygon with the upper layer.
            _offset_geom_coords.reverse()

        return _offset_geom_coords

    def _get_offset_geometry(
        self, offset_geom_coords: List[geometry.Point]
    ) -> geometry.LineString:
        offset_geom_coords.reverse()
        return geometry.LineString(offset_geom_coords)

    def _get_layer_geometry(
        self, offset_geom_coords: List[geometry.Point]
    ) -> geometry.Polygon:
        # Avoid duplicates while preserving order
        _layer_geometry_points = list(dict.fromkeys(self.upper_linestring.coords))
        _layer_geometry_points.extend(offset_geom_coords)
        _layer_geometry_points.append(_layer_geometry_points[0])
        return geometry.Polygon(_layer_geometry_points)

    def build(self) -> KoswatCoatingLayer:
        if not (self.upper_linestring and self.layer_data and self.base_geometry):
            raise ValueError("All coating layer builder fields are required.")

        _depth = self.layer_data.get("depth", math.nan)
        _material_type =self.layer_data["material"]
        if math.isnan(_depth):
            # Usually only for the base layer (sand)
            raise ValueError(
                f"Depth cannot be negative in a coating layer. Layer: {_material_type.name.capitalize()}"
            )

        _offset_geom_coords = self._get_offset_coordinates(_depth)

        # Create the new coating layer
        _layer = KoswatCoatingLayer()
        _layer.upper_points = self.upper_linestring
        _layer.outer_geometry = self.base_geometry
        _layer.material_geometry = remove_layer_from_polygon(self.base_geometry, _depth)
        _layer.lower_linestring = self._get_offset_geometry(_offset_geom_coords)
        _layer.material_type = _material_type
        _layer.depth = _depth
        return _layer
