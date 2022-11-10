from typing import List

from shapely.geometry import Point, Polygon

from koswat.calculations.reinforcement_layers_wrapper import (
    ReinforcementBaseLayer,
    ReinforcementCoatingLayer,
    ReinforcementLayersWrapper,
)
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapperProtocol
from koswat.dike.layers.koswat_layers_wrapper_builder import (
    KoswatLayersWrapperBuilder,
    KoswatLayersWrapperBuilderProtocol,
)
from koswat.geometries.calc_library import (
    get_polygon_surface_points,
    get_relative_core_layer,
)


class StandardReinforcementLayersWrapperBuilder(KoswatLayersWrapperBuilderProtocol):
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

    def _get_base_layer(self, new_layer: KoswatLayerProtocol) -> ReinforcementBaseLayer:
        _reinforced_base_layer = ReinforcementBaseLayer.from_koswat_base_layer(
            new_layer
        )
        _old_geom = Polygon(self.layers_data["base_layer"]["geometry"])
        _added_geometry = new_layer.geometry.difference(_old_geom)
        _reinforced_base_layer.old_layer_geometry = _old_geom
        _reinforced_base_layer.new_layer_geometry = _added_geometry
        _reinforced_base_layer.new_layer_surface = get_polygon_surface_points(
            _added_geometry
        )
        return _reinforced_base_layer

    def _get_coating_layers(
        self, new_coating_layers: KoswatLayerProtocol, relative_core_geom: Polygon
    ) -> List[ReinforcementCoatingLayer]:
        _mapped_layers = list(
            zip(self.layers_data["coating_layers"], new_coating_layers)
        )
        _rc_layer_list: List[ReinforcementCoatingLayer] = []
        _wrapped_calc_geometry = relative_core_geom
        for (_old_coating_data, _new_coating_layer) in reversed(_mapped_layers):
            # Define old and relative geometries.
            _old_geom = Polygon(_old_coating_data["geometry"])
            _relative_core = get_relative_core_layer(relative_core_geom, _old_geom)

            # Calculate the removed geometry.
            _removed_geom = _old_geom.difference(_relative_core)
            if any(_rc_layer_list):
                _removed_geom = _removed_geom.difference(_wrapped_calc_geometry)
            # Calculate the added geometry.
            _added_geometry = _new_coating_layer.geometry.difference(
                _relative_core.union(_wrapped_calc_geometry)
            )
            # Create new Reinforced Coating Layer
            _rc_layer = ReinforcementCoatingLayer.from_koswat_coating_layer(
                _new_coating_layer
            )
            _rc_layer.old_layer_geometry = _old_geom
            _rc_layer.removal_layer_geometry = _removed_geom
            _rc_layer.new_layer_geometry = _added_geometry
            _rc_layer.new_layer_surface = get_polygon_surface_points(_added_geometry)
            _rc_layer_list.append(_rc_layer)

            # Update wrapped calc geometry.
            _wrapped_calc_geometry = _rc_layer.geometry
        return reversed(_rc_layer_list)

    def _get_basic_wrapper(self) -> KoswatLayersWrapperProtocol:
        """
        Returns a wrapper with the basic information of the new geometries.
        """
        _default_builder = KoswatLayersWrapperBuilder()
        _default_builder.layers_data = self.layers_data
        _default_builder.profile_points = self.profile_points
        return _default_builder.build()
