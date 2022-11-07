from shapely.geometry import Polygon

from koswat.cost_report.layer.base_layer_cost_report import BaseLayerCostReport
from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol
from koswat.geometries.calc_library import (
    get_polygon_coordinates,
    get_polygon_surface_points,
)


class OustideSlopeWeakeningLayerCostReportBuilder(LayerCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol

    def __init__(self) -> None:
        # TODO: At the moment this class is a duplicate of `BaseLayerCostReportBuilder`. Consider removing.
        self.base_layer = None
        self.calc_layer = None

    def build(self) -> BaseLayerCostReport:
        if self.base_layer.material.name != self.calc_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        _layer_report = BaseLayerCostReport()
        _layer_report.new_layer = self.calc_layer
        _layer_report.old_layer = self.base_layer
        _layer_report.added_layer = KoswatCoatingLayer()
        _layer_report.added_layer.material = self.calc_layer.material
        _added_geometry = self.calc_layer.geometry.difference(self.base_layer.geometry)
        _layer_report.added_layer.geometry = _added_geometry
        _layer_report.added_layer.layer_points = get_polygon_coordinates(
            _added_geometry
        )
        _layer_report.added_layer.upper_points = get_polygon_surface_points(
            _added_geometry
        )
        return _layer_report
