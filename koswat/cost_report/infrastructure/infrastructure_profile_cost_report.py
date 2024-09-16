import math
from dataclasses import dataclass

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class InfrastructureProfileCostReport(CostReportProtocol):
    reinforced_profile: ReinforcementProfileProtocol

    @property
    def total_cost(self) -> float:
        return math.nan

    @property
    def total_cost_with_surtax(self) -> float:
        return math.nan
