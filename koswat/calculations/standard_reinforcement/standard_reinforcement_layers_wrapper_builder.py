from typing import List

from shapely.geometry import Point, Polygon

from koswat.calculations.reinforcement_layers_wrapper import (
    ReinforcementBaseLayer,
    ReinforcementCoatingLayer,
    ReinforcementLayersWrapper,
)
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.layers.layers_wrapper import (
    KoswatLayersWrapperBuilder,
    KoswatLayersWrapperBuilderProtocol,
    KoswatLayersWrapperProtocol,
)
from koswat.geometries.calc_library import (
    as_unified_geometry,
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
            _reinforcement_layers_wrapper.base_layer,
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
        self,
        new_coating_layers: KoswatLayerProtocol,
        base_layer: ReinforcementBaseLayer,
    ) -> List[ReinforcementCoatingLayer]:
        _mapped_layers = list(
            zip(self.layers_data["coating_layers"], new_coating_layers)
        )
        _rc_layer_list: List[ReinforcementCoatingLayer] = []
        _relative_core_geom = base_layer.old_layer_geometry
        _wrapped_calc_layer = base_layer
        for (_old_coating_data, _new_coating_layer) in reversed(_mapped_layers):
            # Define old and relative geometries.
            _old_geom = Polygon(_old_coating_data["geometry"])
            _relative_core_geom = get_relative_core_layer(
                _relative_core_geom, _old_geom
            )

            # Calculate the removed geometry.
            _removed_geom = _old_geom.difference(_relative_core_geom)
            if any(_rc_layer_list):
                _removed_geom = as_unified_geometry(
                    _removed_geom.difference(_wrapped_calc_layer.old_layer_geometry)
                )
            # Calculate the added geometry.
            _added_geometry = as_unified_geometry(
                _new_coating_layer.geometry.difference(
                    _relative_core_geom.union(_wrapped_calc_layer.geometry)
                )
            )

            from matplotlib import pyplot

            def plot_geometry(geometry):
                _gx, _gy = geometry.boundary.coords.xy
                _subplot.plot(_gx, _gy)

            # _fig = pyplot.figure(dpi=140)
            # _subplot = _fig.add_subplot()
            # _fig.show()
            # plot_geometry(_new_coating_layer.geometry)
            # plot_geometry(_old_geom)
            # plot_geometry(_added_geometry)
            # plot_geometry(_removed_geom)
            # pyplot.close(_fig)

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
            _wrapped_calc_layer = _rc_layer
        return list(reversed(_rc_layer_list))

    def _get_basic_wrapper(self) -> KoswatLayersWrapperProtocol:
        """
        Returns a wrapper with the basic information of the new geometries.
        """
        _default_builder = KoswatLayersWrapperBuilder()
        _default_builder.layers_data = self.layers_data
        _default_builder.profile_points = self.profile_points
        return _default_builder.build()
