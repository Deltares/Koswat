from shapely.geometry import LineString, Point, Polygon

from koswat.calculations import ReinforcementProfileProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class StandardProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_relative_core_layer(
        self, core_geometry: Polygon, coating_layer: KoswatLayerProtocol
    ) -> Polygon:
        # Create a 'fake' base layer geometry to later do proper intersections.
        _core_points = list(core_geometry.boundary.coords)
        _coating_points = list(coating_layer.geometry.boundary.coords)
        _aux_coord = Point(_coating_points[0][0], _core_points[1][1])
        _wrapper_points = LineString(
            [
                _coating_points[0],
                _aux_coord,
                _core_points[1],
                _core_points[0],
                _coating_points[0],
            ]
        )
        _wrapper_polygon = Polygon(_wrapper_points)
        _fixed_layer_geom = _wrapper_polygon.intersection(coating_layer.geometry)
        return _fixed_layer_geom.union(core_geometry)

    def build(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _report.new_profile = self.calculated_profile
        _report.old_profile = self.base_profile
        if len(self.base_profile.layers_wrapper.layers) != len(
            self.calculated_profile.layers_wrapper.layers
        ):
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )

        # Get old_core and new core layer
        _core_layer_report = LayerCostReport()
        _core_layer_report.old_layer = self.base_profile.layers_wrapper.base_layer
        _core_layer_report.new_layer = self.calculated_profile.layers_wrapper.base_layer
        _core_layer_report.added_layer = KoswatCoatingLayer()
        _core_layer_report.added_layer.material = _core_layer_report.old_layer.material
        _core_layer_report.added_layer.geometry = (
            _core_layer_report.new_layer.geometry.difference(
                _core_layer_report.old_layer.geometry
            )
        )
        # _new_base_geom = _core_layer_report.new_layer.geometry
        _report.layer_cost_reports.append(_core_layer_report)
        # Get x_layer_removal and x_layer_added
        for idx_l, _old_coating_layer in reversed(
            list(enumerate(self.base_profile.layers_wrapper.coating_layers))
        ):
            _calculated_coating_layer = (
                self.calculated_profile.layers_wrapper.coating_layers[idx_l]
            )
            _relative_core = self._get_relative_core_layer(
                _report.layer_cost_reports[-1].old_layer.geometry, _old_coating_layer
            )

            # Layer cost report
            _layer_report = StandardLayerCostReport()
            _layer_report.new_layer = _calculated_coating_layer
            _layer_report.old_layer = _old_coating_layer

            # Removed Layer
            _layer_report.removed_layer = KoswatCoatingLayer()
            _layer_report.removed_layer.material = _calculated_coating_layer.material
            _layer_report.removed_layer.geometry = (
                _old_coating_layer.geometry.difference(_relative_core)
            )

            # Added layer
            _new_calculated_geom = _calculated_coating_layer.geometry
            _added_geom = _new_calculated_geom.difference(
                _relative_core.union(_report.layer_cost_reports[-1].new_layer.geometry)
            )
            _layer_report.added_layer = KoswatCoatingLayer()
            _layer_report.added_layer.material = _calculated_coating_layer.material
            _layer_report.added_layer.geometry = _added_geom

            # Add it to collection
            _report.layer_cost_reports.append(_layer_report)

        return _report
