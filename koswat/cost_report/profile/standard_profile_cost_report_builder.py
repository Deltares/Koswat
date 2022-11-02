from shapely import affinity
from shapely.geometry import LineString, Point, Polygon

from koswat.calculations import ReinforcementProfileProtocol
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol
from koswat.geometries import plot_layers, plot_polygons


class StandardProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_layer_cost_report(
        self,
        old_layer: KoswatLayerProtocol,
        new_layer: KoswatLayerProtocol,
        core_layer: KoswatLayerProtocol,
    ) -> StandardLayerCostReport:
        _report = StandardLayerCostReport()
        _report.new_layer = new_layer
        _report.old_layer = old_layer
        _report.core_layer = core_layer
        _report.removed_layer = KoswatBaseLayer()
        _report.removed_layer.geometry = old_layer.geometry.difference(
            core_layer.geometry
        )
        _report.removed_layer.material = new_layer.material
        # pl1 = plot_layers(_report.core_layer, _report.removed_layer)
        # pl2 = plot_layers(_report.core_layer, _report.new_layer)
        return _report

    def _get_base_layer_report(
        self, old_base_layer: KoswatBaseLayer, new_base_layer: KoswatBaseLayer
    ) -> StandardLayerCostReport:
        _report = StandardLayerCostReport()
        _report.old_layer = old_base_layer
        _report.core_layer = old_base_layer
        _report.new_layer = new_base_layer
        _report.removed_layer = None
        # _diff_geometry = new_base_layer.geometry.difference(old_base_layer.geometry)
        # _report.new_layer = KoswatBaseLayer()
        # _report.new_layer.geometry = _diff_geometry
        # _report.new_layer.material = new_base_layer.material
        return _report

    def _get_relative_core_layer(
        self, core_layer: KoswatLayerProtocol, coating_layer: KoswatLayerProtocol
    ) -> KoswatLayerProtocol:
        # Create a 'fake' base layer geometry to later do proper intersections.
        _core_points = list(core_layer.geometry.boundary.coords)
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

        # Create new 'base' layer
        _new_layer = KoswatBaseLayer()
        _new_layer.geometry = _fixed_layer_geom.union(core_layer.geometry)
        _new_layer.material = core_layer.material
        # pl = plot_layers(core_layer, _new_layer)
        # pl = plot_polygons(_fixed_layer_geom, coating_layer.geometry)
        return _new_layer

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

        _core_layer_report = self._get_base_layer_report(
            self.base_profile.layers_wrapper.base_layer,
            self.calculated_profile.layers_wrapper.base_layer,
        )
        _core_layer = _core_layer_report.old_layer
        for idx_l, old_coating_layer in reversed(
            list(enumerate(self.base_profile.layers_wrapper.coating_layers))
        ):
            _new_coating_layer: KoswatLayerProtocol = (
                self.calculated_profile.layers_wrapper.coating_layers[idx_l]
            )
            _core_layer = self._get_relative_core_layer(_core_layer, _new_coating_layer)
            _layer_report = self._get_layer_cost_report(
                old_coating_layer, _new_coating_layer, _core_layer
            )

            _report.layer_cost_reports.append(_layer_report)

        _report.layer_cost_reports.append(_core_layer_report)
        return _report
