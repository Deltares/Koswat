from __future__ import annotations

import math
from typing import List

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameters
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class ProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    volume_cost_parameters: VolumeCostParameters
    layer_cost_reports: List[LayerCostReport]
    _decimals = 2

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.volume_cost_parameters = None
        self.layer_cost_reports = []
        self.volume_cost_parameters = VolumeCostParameters()

    @property
    def total_cost(self) -> float:
        if not self.volume_cost_parameters:
            return math.nan
        return round(
            sum(
                vcp.total_cost() for vcp in self.volume_cost_parameters.get_parameters()
            ),
            self._decimals,
        )

    @property
    def total_volume(self) -> float:
        if not self.volume_cost_parameters:
            return math.nan
        # TODO: This is most likely wrong. Need to be refined (or perhaps removed indeed not needed).
        return round(
            sum(vcp.volume for vcp in self.volume_cost_parameters.get_parameters()),
            self._decimals,
        )
