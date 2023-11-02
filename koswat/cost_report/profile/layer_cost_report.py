from __future__ import annotations

import math

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)


class LayerCostReport(CostReportProtocol):
    layer: ReinforcementLayerProtocol | None
    total_cost: float
    total_cost_with_surtax: float
    total_quantity: float

    def __init__(self) -> None:
        self.layer = None
        self.total_cost = math.nan
        self.total_cost_with_surtax = math.nan
        self.total_quantity = math.nan

    @property
    def material(self) -> str:
        if not self.layer or not self.layer.material_type:
            return ""
        return self.layer.material_type.name
