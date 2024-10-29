from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from koswat.cost_report.multi_location_profile import MultiLocationProfileCostReport
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class KoswatSummary:
    locations_profile_report_list: list[MultiLocationProfileCostReport] = field(
        default_factory=lambda: []
    )
    reinforcement_per_locations: list[StrategyLocationReinforcement] = field(
        default_factory=lambda: []
    )

    def get_report_by_profile(
        self, profile_type: type[ReinforcementProfileProtocol]
    ) -> MultiLocationProfileCostReport | None:
        """
        Get the report for a specific profile type.

        Args:
            profile_type (type[ReinforcementProfileProtocol]): Type of reinforcement profile.

        Returns:
            MultiLocationProfileCostReport | None: Report for the profile type.
        """
        return next(
            (
                _report
                for _report in self.locations_profile_report_list
                if isinstance(
                    _report.profile_cost_report.reinforced_profile, profile_type
                )
            ),
            None,
        )

    def get_infrastructure_costs(
        self,
    ) -> dict[type[ReinforcementProfileProtocol], tuple[float, float]]:
        """
        Gets the infrastructure costs for each profile type
        for those locations for which the profile type is selected.

        Returns:
            dict[type[ReinforcementProfileProtocol], tuple[float, float]]:
                infrastructure costs without and with surtax per reinforcement type.
        """
        _infra_costs_per_reinforcement = defaultdict(tuple)

        # Get the infra cost tuples (without and with surtax) for each location.
        _infra_costs_dict = defaultdict(list)
        for _loc in self.reinforcement_per_locations:
            _infra_costs_dict[_loc.selected_measure].append(
                _loc.get_infrastructure_costs(_loc.selected_measure)
            )

        # Sum the infra costs for each reinforcement type.
        for _rt, _infra_costs in _infra_costs_dict.items():
            _infra_costs, _infra_costs_with_surtax = zip(*_infra_costs)
            _infra_costs_per_reinforcement[_rt] = (
                sum(_infra_costs),
                sum(_infra_costs_with_surtax),
            )

        return dict(_infra_costs_per_reinforcement)
