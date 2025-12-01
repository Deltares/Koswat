"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

import math
from typing import List

from shapely import geometry

from koswat.core.geometries.calc_library import remove_layer_from_polygon
from koswat.dike.layers.coating_layer.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol


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
        # We round to 3 decimals (mm) to avoid precission issues when computing the geometries differences.
        _offset_geom_coords = [
            (round(x, 3), round(y, 3)) for x, y in _offset_geom_linestring.coords
        ]
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
        _material_type = self.layer_data["material"]
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
