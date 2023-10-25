from __future__ import annotations

from dataclasses import dataclass, field

from koswat.cost_report.multi_location_profile import MultiLocationProfileCostReport
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.strategies.strategy_location_matrix import StrategyLocationReinforcements


@dataclass
class KoswatSummary:
    locations_profile_report_list: list[MultiLocationProfileCostReport] = field(
        default_factory=lambda: []
    )
    available_locations: list[PointSurroundings] = field(default_factory=lambda: [])
    reinforcement_per_locations: list[StrategyLocationReinforcements] = field(
        default_factory=lambda: []
    )
