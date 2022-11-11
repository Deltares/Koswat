from __future__ import annotations

import math
from typing import List

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.volume_cost_parameters import VolumeCostParameters


class ProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    volume_cost_parameters: VolumeCostParameters

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.volume_cost_parameters = None

    @classmethod
    def build(
        cls, reinforced_profile: ReinforcementProfileProtocol
    ) -> ProfileCostReport:
        _report = cls()
        _report.volume_cost_parameters = VolumeCostParameters.from_reinforced_profile(
            reinforced_profile
        )
        _report.reinforced_profile = reinforced_profile

        return _report

    @property
    def total_cost(self) -> float:
        return sum(
            vcp.total_cost() for vcp in self.volume_cost_parameters.get_parameters()
        )

    @property
    def total_volume(self) -> float:
        # TODO: This is most likely wrong. Need to be refined (or perhaps removed indeed not needed).
        return sum(vcp.volume for vcp in self.volume_cost_parameters.get_parameters())

    def get_layers_report(self) -> List[CostReportProtocol]:
        return []
