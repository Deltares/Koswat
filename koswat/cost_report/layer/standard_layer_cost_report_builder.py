from shapely.geometry import LineString, Point, Polygon

from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class StandardLayerCostReportBuilder(LayerCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol
    base_core_geometry: Polygon
    calc_core_geometry: Polygon

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None
        self.base_core_geometry = None
        self.calc_core_geometry = None

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
        return Polygon(_fixed_layer_geom.union(core_geometry))

    def build(self) -> StandardLayerCostReport:
        if self.base_layer.material.name != self.calc_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")

        # Layer cost report
        _layer_report = StandardLayerCostReport()
        _layer_report.new_layer = self.calc_layer
        _layer_report.old_layer = self.base_layer

        # Removed Layer
        _layer_report.removed_layer = KoswatCoatingLayer()
        _layer_report.removed_layer.material = self.calc_layer.material
        _layer_report.removed_layer.geometry = self.base_layer.geometry.difference(
            self.base_core_geometry
        )

        # Added layer
        _new_calculated_geom = self.calc_layer.geometry
        _added_geom = _new_calculated_geom.difference(
            self.base_core_geometry.union(self.calc_core_geometry)
        )
        _layer_report.added_layer = KoswatCoatingLayer()
        _layer_report.added_layer.material = self.calc_layer.material
        _layer_report.added_layer.geometry = _added_geom

        return _layer_report
