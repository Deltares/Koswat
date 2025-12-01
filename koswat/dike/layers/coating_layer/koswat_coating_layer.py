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

from shapely.geometry import LineString, Polygon

from koswat.core.geometries.calc_library import (
    get_polygon_coordinates,
    order_geometry_points,
)
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class KoswatCoatingLayer(KoswatLayerProtocol):
    depth: float
    lower_linestring: LineString
    upper_points: LineString
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.lower_linestring = None
        self.upper_points = None
        self.material_geometry = None
        self.depth = math.nan

    def get_coated_geometry(self) -> Polygon:
        if not self.material_geometry or not self.outer_geometry:
            return None
        return order_geometry_points(
            self.outer_geometry.difference(self.material_geometry)
        )

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type,
            depth=self.depth,
            geometry=_geometry,
        )
