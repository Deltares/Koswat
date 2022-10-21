from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.layer.layer_cost_report_builder import (
    LayerCostReportBuilderProtocol,
)
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class StandardLayerCostReportBuilder(LayerCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None

    def build(self) -> LayerCostReport:
        if self.base_layer.material.name != self.calc_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        _layer_report = LayerCostReport()
        _diff_geometry = self.calc_layer.geometry.difference(self.base_layer.geometry)
        _layer_report.total_volume = _diff_geometry.area
        _layer_report.new_layer = self.calc_layer
        _layer_report.old_layer = self.base_layer
        return _layer_report
