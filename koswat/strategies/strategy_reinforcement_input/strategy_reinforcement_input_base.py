"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

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

from abc import ABC
from dataclasses import dataclass
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from .strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)


@dataclass(kw_only=True)
class StrategyReinforcementInputBase(ABC, StrategyReinforcementInputProtocol):
    """
    A strategy reinforcement input aimed for those reinforcements that can use both
    polder- and waterside space.
    """

    reinforcement_type: type[ReinforcementProfileProtocol]
    active: bool = True
    base_costs_with_surtax: float = 0.0
    ground_level_surface: float = 0.0

    def _has_greater_costs_than(
        self, other: StrategyReinforcementInputProtocol
    ) -> bool:
        return self.base_costs_with_surtax > other.base_costs_with_surtax

    def _has_greater_or_equal_ground_level_surface_than(
        self, other: StrategyReinforcementInputProtocol
    ) -> bool:
        return self.ground_level_surface >= other.ground_level_surface

    def is_more_cost_space_restrictive(
        self, other: StrategyReinforcementInputProtocol
    ) -> bool:
        # For now we only apply this criteria for `OrderStrategy` filtering.
        # if we wish to do so in other strategies, we can add a `criteria` argument to this method.
        # criteria: Callable[['StrategyReinforcementInput', 'StrategyReinforcementInput'], bool]
        return self._has_greater_costs_than(
            other
        ) and self._has_greater_or_equal_ground_level_surface_than(other)
