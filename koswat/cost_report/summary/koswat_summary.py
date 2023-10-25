from __future__ import annotations
from dataclasses import field, dataclass
from typing import Type
from koswat.cost_report.multi_location_profile import MultiLocationProfileCostReport
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import ReinforcementProfileProtocol
from koswat.strategies.strategy_location_matrix import StrategyLocationReinforcements

@dataclass
class KoswatSummary:
    locations_profile_report_list: list[MultiLocationProfileCostReport] = field(default_factory=lambda: [])
    reinforcement_per_locations: list[StrategyLocationReinforcements] = field(default_factory=lambda: [])

    def get_report_by_profile(self, profile_type: Type[ReinforcementProfileProtocol]) -> MultiLocationProfileCostReport | None:
        return next((_report for _report in self.locations_profile_report_list if isinstance(_report.profile_cost_report.reinforced_profile, profile_type)), None)
