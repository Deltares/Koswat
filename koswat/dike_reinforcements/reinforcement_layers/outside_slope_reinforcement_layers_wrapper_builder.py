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

from shapely.geometry import Point, Polygon

from koswat.core.geometries.calc_library import get_polygon_surface_points
from koswat.dike.layers import KoswatLayerProtocol
from koswat.dike.layers.base_layer import KoswatBaseLayer
from koswat.dike.layers.coating_layer import KoswatCoatingLayer
from koswat.dike.layers.layers_wrapper import (
    KoswatLayersWrapperBuilder,
    KoswatLayersWrapperBuilderProtocol,
    KoswatLayersWrapperProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_base_layer import (
    ReinforcementBaseLayer,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_coating_layer import (
    ReinforcementCoatingLayer,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)


class OutsideSlopeReinforcementLayersWrapperBuilder(KoswatLayersWrapperBuilderProtocol):
    layers_data: dict  # Previous profile layers wrapper
    profile_points: list[Point]  # Characteristic points.

    def build(self) -> ReinforcementLayersWrapper:
        _reinforcement_layers_wrapper = ReinforcementLayersWrapper()
        _koswat_layers_wrapper = self._get_basic_wrapper()
        _reinforced_layers = self._get_reinforced_layers(_koswat_layers_wrapper)
        _reinforcement_layers_wrapper.base_layer = next(
            rl for rl in _reinforced_layers if isinstance(rl, ReinforcementBaseLayer)
        )
        _reinforcement_layers_wrapper.coating_layers = [
            rl for rl in _reinforced_layers if isinstance(rl, ReinforcementCoatingLayer)
        ]
        return _reinforcement_layers_wrapper

    def _get_reinforced_layers(
        self, layers_wrapper: KoswatLayersWrapperProtocol
    ) -> list[ReinforcementLayerProtocol]:
        _mapped_layers = list(
            zip(self.layers_data["coating_layers"], layers_wrapper.coating_layers)
        )
        _mapped_layers.append(
            (self.layers_data["base_layer"], layers_wrapper.base_layer)
        )
        _add_layers_reference = [
            _layer.outer_geometry for _layer in layers_wrapper.layers[1:]
        ]
        _add_layers_reference.append(
            Polygon(self.layers_data["base_layer"]["geometry"])
        )
        _reinforcement_list: list[ReinforcementLayerProtocol] = []
        for idx, (_base_layer_data, _calc_layer) in enumerate(_mapped_layers):
            _core_idx = min(idx + 1, len(_mapped_layers) - 1)
            _base_core, _ = _mapped_layers[_core_idx]
            _calc_core_geom = _add_layers_reference[idx]
            _reinforced_layer = self._get_reinforced_layer(
                _calc_layer,
                Polygon(_base_layer_data["geometry"]),
                Polygon(_base_core["geometry"]),
                _calc_core_geom,
            )
            _reinforcement_list.append(_reinforced_layer)
        return _reinforcement_list

    def _get_reinforced_layer(
        self,
        new_layer: KoswatLayerProtocol,
        old_geom: dict,
        base_core_geom: Polygon,
        calc_core_geom: Polygon,
    ) -> ReinforcementLayerProtocol:
        # Removed Layer
        if isinstance(new_layer, KoswatCoatingLayer):
            return self._get_coating_layer(
                new_layer, old_geom, calc_core_geom, base_core_geom
            )
        elif isinstance(new_layer, KoswatBaseLayer):
            return self._get_base_layer(new_layer, old_geom, calc_core_geom)
        else:
            raise NotImplementedError(f"Layer type not recognized {new_layer}")

    def _get_base_layer(
        self,
        new_layer: KoswatLayerProtocol,
        old_geometry: Polygon,
        calc_geometry: Polygon,
    ) -> ReinforcementBaseLayer:
        _reinforced_base_layer = ReinforcementBaseLayer.from_koswat_base_layer(
            new_layer
        )
        # New Geometry (Added volume)
        _added_geometry = new_layer.outer_geometry.difference(calc_geometry)

        _reinforced_base_layer.old_layer_geometry = old_geometry
        _reinforced_base_layer.new_layer_geometry = _added_geometry
        _reinforced_base_layer.new_layer_surface = get_polygon_surface_points(
            _added_geometry
        )
        return _reinforced_base_layer

    def _get_coating_layer(
        self,
        new_layer: KoswatLayerProtocol,
        old_geometry: Polygon,
        calc_geometry: Polygon,
        base_core_geometry: Polygon,
    ) -> list[ReinforcementCoatingLayer]:
        if old_geometry == new_layer.outer_geometry:
            # KOSWAT_82: For now, we assume that the depth of layers remains the same
            # as from the input profile base.
            return ReinforcementCoatingLayer.with_same_outer_geometry(new_layer)

        # Create new Reinforced Coating Layer
        _rc_layer = ReinforcementCoatingLayer.from_koswat_coating_layer(new_layer)
        _rc_layer.old_layer_geometry = old_geometry

        # Removed geometry (Removal volume)
        _rc_layer.removal_layer_geometry = _rc_layer.old_layer_geometry.difference(
            base_core_geometry
        )

        # New Geometry (Added volume)
        _added_geometry = new_layer.outer_geometry.difference(calc_geometry)
        _rc_layer.new_layer_geometry = _added_geometry
        _rc_layer.new_layer_surface = get_polygon_surface_points(_added_geometry)

        return _rc_layer

    def _get_basic_wrapper(self) -> KoswatLayersWrapperProtocol:
        """
        Returns a wrapper with the basic information of the new geometries.
        """
        _default_builder = KoswatLayersWrapperBuilder()
        _default_builder.layers_data = self.layers_data
        _default_builder.profile_points = self.profile_points
        return _default_builder.build()
