from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from koswat.cost_report.multi_location_profile import MultiLocationProfileCostReport
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
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

    def get_locations_by_profile(
        self,
    ) -> dict[type[ReinforcementProfileProtocol], list[PointSurroundings]]:
        """
        Get the locations per selected profile type.

        Returns:
            dict[type[ReinforcementProfileProtocol], list[PointSurroundings]]:
        """
        _locs_per_reinforcements: dict[
            type[ReinforcementProfileProtocol], list[PointSurroundings]
        ] = defaultdict(list)

        for _loc in self.reinforcement_per_locations:
            _locs_per_reinforcements[_loc.selected_measure].append(_loc.location)

        return dict(_locs_per_reinforcements)

    def get_infra_costs_by_profile(
        self,
    ) -> defaultdict[type[ReinforcementProfileProtocol], tuple[float, float]]:
        """
        Gets the infrastructure costs for each profile type
        for the locations for which the profile type is selected.

        Returns:
            defaultdict[type[ReinforcementProfileProtocol], tuple[float, float]]:
                infra cost without and with surtax per reinforcement type.
        """
        _locs_per_reinforcements = self.get_locations_by_profile()

        _infra_cost_per_reinforcement = defaultdict(lambda: (0.0, 0.0))
        for _rt, _locs in _locs_per_reinforcements.items():
            _infra_cost_list, _infra_cost_with_surtax_list = zip(
                *(
                    (_impcr.total_cost, _impcr.total_cost_with_surtax)
                    for _lprl in self.locations_profile_report_list
                    for _impcr in _lprl.infra_multilocation_profile_cost_report
                    if _impcr.location in _locs
                )
            )

            _infra_cost_per_reinforcement[_rt] = (
                sum(_infra_cost_list),
                sum(_infra_cost_with_surtax_list),
            )

        return _infra_cost_per_reinforcement

    def get_infrastructure_cost(
        self, profile_type: type[ReinforcementProfileProtocol]
    ) -> float:
        """
        Get the infrastructure cost for those locations for which a specific profile type is selected.

        Args:
            profile_type (type[ReinforcementProfileProtocol]): Type of reinforcement profile.

        Returns:
            float: Infrastructure cost.
        """
        _locations = self.get_locations_by_profile(profile_type)
        if not _locations:
            return 0.0
        _report = self.get_report_by_profile(profile_type)
        return sum(
            ilpcr.total_cost
            for ilpcr in _report.infra_multilocation_profile_cost_report
            if ilpcr.location in _locations
        )

    def get_infrastructure_cost_with_surtax(
        self, profile_type: type[ReinforcementProfileProtocol]
    ) -> float:
        _locations = self.get_locations_by_profile(profile_type)
        if not _locations:
            return 0.0
        _report = self.get_report_by_profile(profile_type)
        return sum(
            ilpcr.total_cost_with_surtax
            for ilpcr in _report.infra_multilocation_profile_cost_report
            if ilpcr.location in _locations
        )
