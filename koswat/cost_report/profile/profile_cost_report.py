from __future__ import annotations

import math
from dataclasses import dataclass, field

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.quantity_cost_parameters import QuantityCostParameters
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class ProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol = None
    quantity_cost_parameters: QuantityCostParameters = field(
        default_factory=QuantityCostParameters
    )
    layer_cost_reports: list[LayerCostReport] = field(default_factory=lambda: [])

    @property
    def total_cost(self) -> float:
        if not self.quantity_cost_parameters:
            return math.nan
        return sum(
            qcp.total_cost for qcp in self.quantity_cost_parameters.get_parameters()
        )

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.quantity_cost_parameters:
            return math.nan
        return sum(
            qcp.total_cost_with_surtax
            for qcp in self.quantity_cost_parameters.get_parameters()
        )
