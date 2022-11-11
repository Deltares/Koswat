import math
from typing import List

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.cost_report_protocol import CostReportProtocol


class ProfileCostReport(CostReportProtocol):
    layer_cost_reports: List[CostReportProtocol]
    reinforced_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.layer_cost_reports = []
        self.new_profile = None
        self.old_profile = None

    @property
    def total_cost(self) -> float:
        return math.nan
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_cost for lr in self.layer_cost_reports)

    @property
    def total_volume(self) -> float:
        return math.nan
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_volume for lr in self.layer_cost_reports)
