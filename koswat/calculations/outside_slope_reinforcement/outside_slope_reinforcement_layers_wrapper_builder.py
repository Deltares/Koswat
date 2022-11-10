from typing import List

from shapely.geometry import Point, Polygon

from koswat.calculations.reinforcement_layers_wrapper import (
    ReinforcementBaseLayer,
    ReinforcementCoatingLayer,
    ReinforcementLayerProtocol,
    ReinforcementLayersWrapper,
)
from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.layers.koswat_layers_wrapper_builder import (
    KoswatLayersWrapperBuilder,
    KoswatLayersWrapperBuilderProtocol,
)
from koswat.geometries.calc_library import get_polygon_surface_points


class OutsideSlopeReinforcementLayersWrapperBuilder(KoswatLayersWrapperBuilderProtocol):
    layers_data: dict  # Previous profile layers wrapper
    profile_points: List[Point]  # Characteristic points.

    def build(self) -> ReinforcementLayersWrapper:
        _reinforcement_layers_wrapper = ReinforcementLayersWrapper()
        _koswat_layers_wrapper = self._get_basic_wrapper()

        _reinforcement_layers_wrapper.base_layer = self._get_base_layer(
            _koswat_layers_wrapper.base_layer
        )
        _reinforcement_layers_wrapper.coating_layers = self._get_coating_layers(
            _koswat_layers_wrapper.coating_layers,
            _reinforcement_layers_wrapper.base_layer.old_layer_geometry,
        )

        return _reinforcement_layers_wrapper

    def _get_reinforced_layers(
        self, layers_wrapper: KoswatLayersWrapperProtocol
    ) -> List[ReinforcementLayerProtocol]:
        _mapped_layers = list(
            zip(self.layers_data["coating_layers"], layers_wrapper.coating_layers)
        )
        _mapped_layers.append(
            (self.layers_data["base_layer"], layers_wrapper.base_layer)
        )
        _add_layers_reference = [
            _layer.geometry for _layer in layers_wrapper.layers[1:]
        ]
        _add_layers_reference.append(
            Polygon(self.layers_data["base_layer"]["geometry"])
        )
        _reinforcement_list = List[ReinforcementLayerProtocol] = []
        for idx, (_base_layer_data, _calc_layer) in enumerate(_mapped_layers):
            _core_idx = min(idx + 1, len(_mapped_layers) - 1)
            _base_core, _ = _mapped_layers[_core_idx]
            _calc_core_geom = _add_layers_reference[idx]
            _reinforced_layer = self._get_reinforced_layer(
                _base_layer_data, _calc_layer, _base_core.geometry, _calc_core_geom
            )
            _reinforcement_list.append(_reinforced_layer)
        return _reinforcement_list

    def _get_reinforced_layer(
        self,
        layer_data: dict,
        new_layer: KoswatLayerProtocol,
        base_core_geom: Polygon,
        calc_core_geom: Polygon,
    ) -> ReinforcementLayerProtocol:
        # Removed Layer
        _old_geom = Polygon(layer_data["base_layer"]["geometry"])
        if isinstance(new_layer, KoswatCoatingLayer):
            return self._get_coating_layer(new_layer, calc_core_geom, base_core_geom)
        elif isinstance(new_layer, KoswatBaseLayer):
            return self._get_base_layer(
                new_layer, _old_geom, calc_core_geom, base_core_geom
            )
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
        _reinforced_base_layer.old_layer_geometry = old_geometry
        # New Geometry (Added volume)
        _added_geometry = new_layer.geometry.difference(calc_geometry)
        _reinforced_base_layer.new_geometry = _added_geometry
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
    ) -> List[ReinforcementCoatingLayer]:
        # Create new Reinforced Coating Layer
        _rc_layer = ReinforcementCoatingLayer.from_koswat_coating_layer(new_layer)
        _rc_layer.old_layer_geometry = old_geometry

        # Removed geometry (Removal volume)
        _rc_layer.removal_layer_geometry = _rc_layer.old_layer_geometry.difference(
            base_core_geometry
        )

        # New Geometry (Added volume)
        _added_geometry = new_layer.geometry.difference(calc_geometry)
        _rc_layer.new_geometry = _added_geometry
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
