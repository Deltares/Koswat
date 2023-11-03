from __future__ import annotations

import math
from typing import List

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.quantity_cost_parameters import QuantityCostParameters
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class ProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    quantity_cost_parameters: QuantityCostParameters
    layer_cost_reports: List[LayerCostReport]

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.quantity_cost_parameters = None
        self.layer_cost_reports = []
        self.quantity_cost_parameters = QuantityCostParameters()

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
