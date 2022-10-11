import math
from typing import List

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class ProfileCostReport(CostReportProtocol):
    layer_cost_reports: List[LayerCostReport]
    new_profile: KoswatProfileBase
    old_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.layer_cost_reports = []
        self.new_profile = None
        self.old_profile = None

    @property
    def total_cost(self) -> float:
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_cost for lr in self.layer_cost_reports)

    @property
    def total_volume(self) -> float:
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_volume for lr in self.layer_cost_reports)
