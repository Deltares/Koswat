"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


@dataclass
class InfraCluster:
    """
    This dataclass represents the subset of locations sharing the same
    reinforcement type (`type[ReinforcementProfileProtocol]`).
    """

    reinforcement_type: type[ReinforcementProfileProtocol]
    min_required_length: int
    cluster: list[StrategyLocationReinforcement] = field(default_factory=lambda: [])

    def is_valid(self) -> bool:
        """
        Validates the length of this cluster.

        Returns:
            bool: The cluster has the minimal required length.
        """
        if not self.cluster:
            return False
        return len(self.cluster) >= self.min_required_length

    def fits_subclusters(self) -> bool:
        """
        Validates whether this cluster can be split into subclusters.
        For that it requires to have at least twice the required length.

        Returns:
            bool: Whether subclusters can be generated from this one.
        """
        return self.is_valid() and len(self.cluster) >= 2 * self.min_required_length

    @property
    def current_cost(self) -> float:
        """
        Calculates the cost of applying the `reinforcement_type` to
        all locations present in the `cluster`.

        Returns:
            float: The total (current) cost of this cluster.
        """
        if not self.cluster:
            return float("nan")
        return sum(_c.current_cost for _c in self.cluster)

    def set_cheapest_common_available_measure(
        self,
        measure_costs: dict[type[ReinforcementProfileProtocol], float],
    ) -> None:
        """
        Updates all the location reinforcements with the cheapest reinforcement type
        from the `measure_costs`.

        Args:
            measure_costs (dict[type[ReinforcementProfileProtocol]]):
                dictionary with the total costs per reinforcement type.
        """
        _selection = min(
            measure_costs,
            key=measure_costs.get,
        )

        if _selection != self.reinforcement_type:
            self.reinforcement_type = _selection
            for _cd in self.cluster:
                _cd.set_selected_measure(_selection, StrategyStepEnum.INFRASTRUCTURE)
