import math

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.profiles.koswat_layers import KoswatLayerProtocol


class LayerCostReport(CostReportProtocol):
    new_layer: KoswatLayerProtocol
    old_layer: KoswatLayerProtocol
    total_volume: float

    def __init__(self) -> None:
        self.new_layer = None
        self.old_layer = None
        self.total_volume = math.nan

    @property
    def total_cost(self) -> float:
        if not self.new_layer:
            return math.nan
        return self.total_volume * self.new_layer.material.cost

    def as_dict(self) -> dict:
        return dict(
            material=self.new_layer.material.name,
            total_volume=self.total_volume,
            total_cost=self.total_cost,
        )
