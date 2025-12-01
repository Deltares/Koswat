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
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


class ReinforcementCoatingLayer(ReinforcementLayerProtocol):
    material_type: KoswatMaterialType
    outer_geometry: Polygon
    material_geometry: Polygon
    upper_points: LineString
    old_layer_geometry: Polygon
    new_layer_geometry: Polygon | MultiPolygon
    new_layer_surface: LineString
    removal_layer_geometry: Polygon

    def __init__(self) -> None:
        self.material_type = None
        self.outer_geometry = None
        self.material_geometry = None
        self.upper_points = None
        self.new_layer_geometry = None
        self.removal_layer_geometry = None

    def as_data_dict(self) -> dict:
        _geometry = []
        if self.outer_geometry:
            _geometry = list(get_polygon_coordinates(self.outer_geometry).coords)
        return dict(
            material=self.material_type.name,
            depth=self.depth,
            geometry=_geometry,
        )

    @classmethod
    def from_koswat_coating_layer(
        cls, coating_layer: KoswatCoatingLayer
    ) -> ReinforcementCoatingLayer:
        _reinforced_coating_layer = cls()
        _reinforced_coating_layer.__dict__ = coating_layer.__dict__
        return _reinforced_coating_layer

    @classmethod
    def with_same_outer_geometry(
        cls, coating_layer: KoswatCoatingLayer
    ) -> ReinforcementCoatingLayer:
        """
        Creates a new reinforcement coating layer which does not differ
        in geometry from the provided coating layer. This was found to
        be needed in KOSWAT_82.

        Args:
            coating_layer (KoswatCoatingLayer): Base coating layer.

        Returns:
            ReinforcementCoatingLayer: Resulting coating layer with "empty"
            polygons for added / removed (layer) geometries.
        """
        _reinforced_coating_layer = cls.from_koswat_coating_layer(coating_layer)
        _reinforced_coating_layer.old_layer_geometry = coating_layer.outer_geometry
        _reinforced_coating_layer.removal_layer_geometry = Polygon()
        _reinforced_coating_layer.new_layer_geometry = Polygon()
        _reinforced_coating_layer.new_layer_surface = LineString()
        return _reinforced_coating_layer
