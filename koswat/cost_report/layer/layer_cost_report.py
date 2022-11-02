import math

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class LayerCostReport(CostReportProtocol):
    new_layer: KoswatLayerProtocol
    old_layer: KoswatLayerProtocol
    added_layer: KoswatLayerProtocol

    def __init__(self) -> None:
        self.new_layer = None
        self.old_layer = None
        self.added_layer = None

    @property
    def total_volume(self) -> float:
        if not self.added_layer:
            return math.nan
        return self.added_layer.geometry.area

    @property
    def total_cost(self) -> float:
        if not self.new_layer:
            return math.nan
        return self.total_volume * self.new_layer.material.cost

    @property
    def material(self) -> str:
        if not self.new_layer or not self.new_layer.material:
            return ""
        return self.new_layer.material.name
