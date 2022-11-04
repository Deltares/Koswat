from shapely.geometry import Polygon

from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class StandardLayerCostReportBuilder(LayerCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol
    added_to_core_geometry: Polygon
    removed_from_core_geometry: Polygon

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None
        self.added_to_core_geometry = None
        self.removed_from_core_geometry = None

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
        _layer_report.removed_layer.geometry = self.removed_from_core_geometry

        # Added layer
        _layer_report.added_layer = KoswatCoatingLayer()
        _layer_report.added_layer.material = self.calc_layer.material
        _layer_report.added_layer.geometry = self.added_to_core_geometry

        return _layer_report
