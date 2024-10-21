from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Type

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
        self, profile_type: Type[ReinforcementProfileProtocol]
    ) -> MultiLocationProfileCostReport | None:
        """
        Get the report for a specific profile type.

        Args:
            profile_type (Type[ReinforcementProfileProtocol]): Type of reinforcement profile.

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
        self, profile_type: Type[ReinforcementProfileProtocol]
    ) -> list[PointSurroundings]:
        """
        Get the locations for which a specific profile type is selected.

        Args:
            profile_type (Type[ReinforcementProfileProtocol]): Type of reinforcement profile.

        Returns:
            list[PointSurroundings]: List of locations.
        """
        return [
            _rpl.location
            for _rpl in self.reinforcement_per_locations
            if _rpl.selected_measure == profile_type
        ]

    def get_infrastructure_cost(
        self, profile_type: Type[ReinforcementProfileProtocol]
    ) -> float:
        """
        Get the infrastructure cost for those locations for which a specific profile type is selected.

        Args:
            profile_type (Type[ReinforcementProfileProtocol]): Type of reinforcement profile.

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
        self, profile_type: Type[ReinforcementProfileProtocol]
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
