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

from __future__ import annotations

from shapely.geometry import LineString, MultiPolygon, Polygon

from koswat.core.geometries.calc_library import get_polygon_coordinates
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


class ReinforcementBaseLayer(ReinforcementLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    old_layer_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None
        self.new_layer_geometry = None

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type.name,
            geometry=_geometry,
        )

    @classmethod
    def from_koswat_base_layer(
        cls, base_layer: KoswatBaseLayer
    ) -> ReinforcementBaseLayer:
        _reinforced_base_layer = cls()
        _reinforced_base_layer.__dict__ = base_layer.__dict__
        return _reinforced_base_layer
