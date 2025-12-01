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

from __future__ import annotations

from typing import List

from shapely import geometry

from koswat.core.geometries.calc_library import profile_points_to_polygon
from koswat.dike.layers.base_layer import KoswatBaseLayer, KoswatBaseLayerBuilder
from koswat.dike.layers.coating_layer import (
    KoswatCoatingLayer,
    KoswatCoatingLayerBuilder,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper import KoswatLayersWrapper
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder_protocol import (
    KoswatLayersWrapperBuilderProtocol,
)


class KoswatLayersWrapperBuilder(KoswatLayersWrapperBuilderProtocol):
    layers_data: dict
    profile_points: List[geometry.Point]
    profile_geometry: geometry.Polygon

    def __init__(self) -> None:
        self.layers_data = {}
        self.profile_points = []
        self.profile_geometry = None

    def _get_coating_layers(self) -> List[KoswatCoatingLayer]:
        _c_layers_data = self.layers_data.get("coating_layers", [])
        if not _c_layers_data:
            return []
        _builder = KoswatCoatingLayerBuilder()
        _builder.upper_linestring = geometry.LineString(self.profile_points)
        _builder.base_geometry = profile_points_to_polygon(self.profile_points)
        _layers = []
        for c_layer_data in _c_layers_data:
            _builder.layer_data = c_layer_data
            _c_layer = _builder.build()
            _builder.base_geometry = _c_layer.get_coated_geometry()
            _builder.upper_linestring = _c_layer.lower_linestring
            _layers.append(_c_layer)
        return _layers

    def _get_base_layer(self, upper_linestring: geometry.LineString) -> KoswatBaseLayer:
        _builder = KoswatBaseLayerBuilder()
        _builder.layer_data = self.layers_data["base_layer"]
        _builder.upper_linestring = upper_linestring
        return _builder.build()

    def build(self) -> KoswatLayersWrapper:
        _koswat_layers = KoswatLayersWrapper()
        _koswat_layers.coating_layers = self._get_coating_layers()
        _base_layer_surface = (
            _koswat_layers.coating_layers[-1].lower_linestring
            if any(_koswat_layers.coating_layers)
            else geometry.LineString(self.profile_points)
        )
        _koswat_layers.base_layer = self._get_base_layer(_base_layer_surface)
        return _koswat_layers
