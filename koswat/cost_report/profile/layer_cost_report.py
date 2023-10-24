from __future__ import annotations

import math

from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)
from koswat.cost_report.cost_report_protocol import CostReportProtocol


class LayerCostReport(CostReportProtocol):
    layer: ReinforcementLayerProtocol
    total_cost: float
    total_volume: float

    def __init__(self) -> None:
        self.layer = None
        self.total_cost = math.nan
        self.total_volume = math.nan

    @property
    def material(self) -> str:
        if not self.layer or not self.layer.material_type:
            return ""
        return self.layer.material_type.name
