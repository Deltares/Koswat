from __future__ import annotations

import math
from typing import List

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.volume_calculation_parameters import (
    VolumeCalculationParameters,
)


class ProfileCostReport(CostReportProtocol):
    layer_cost_reports: List[CostReportProtocol]
    reinforced_profile: ReinforcementProfileProtocol
    volume_calculation_parameters: VolumeCalculationParameters

    def __init__(self) -> None:
        self.layer_cost_reports = []
        self.reinforced_profile = None
        self.volume_calculation_parameters = None

    @classmethod
    def build(
        cls, reinforced_profile: ReinforcementProfileProtocol
    ) -> ProfileCostReport:
        _report = cls()
        _report.volume_calculation_parameters = (
            VolumeCalculationParameters.from_reinforced_profile(reinforced_profile)
        )
        _report.reinforced_profile = reinforced_profile

        return _report

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
