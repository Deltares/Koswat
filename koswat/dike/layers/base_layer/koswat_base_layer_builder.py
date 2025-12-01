"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

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

from shapely import geometry

from koswat.core.geometries.calc_library import profile_points_to_polygon
from koswat.dike.layers.base_layer.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_layer_builder_protocol import KoswatLayerBuilderProtocol


class KoswatBaseLayerBuilder(KoswatLayerBuilderProtocol):
    layer_data: dict
    upper_linestring: geometry.LineString

    def __init__(self) -> None:
        self.layer_data = {}
        self.upper_linestring = None

    def build(self) -> KoswatBaseLayer:
        if not self.upper_linestring:
            raise ValueError("Profile line geometry needs to be provided.")
        _material_type = self.layer_data.get("material", None)
        if not _material_type:
            raise ValueError("Material data needs to be provided.")

        _layer = KoswatBaseLayer()
        _layer.outer_geometry = profile_points_to_polygon(
            list(map(geometry.Point, self.upper_linestring.coords))
        )
        _layer.material_type = _material_type
        _layer.upper_points = self.upper_linestring
        return _layer
