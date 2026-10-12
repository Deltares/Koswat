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

from __future__ import annotations
from typing import Protocol
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class StrategyReinforcementInputProtocol(Protocol):
    """
    A strategy reinforcement input is a reinforcement that can be used in a strategy.
    It contains the reinforcement type, whether it is active, the base costs with surtax,
    and the ground level surface.
    """

    reinforcement_type: type[ReinforcementProfileProtocol]
    active: bool
    base_costs_with_surtax: float
    ground_level_surface: float

    def is_more_cost_space_restrictive(
        self, other: StrategyReinforcementInputProtocol
    ) -> bool:
        """
        Determines if this reinforcement input is more restrictive than another
        based on costs and ground level surface.

        Args:
            other (StrategyReinforcementInputProtocol): The other reinforcement input to compare against.

        Returns:
            bool: True if this reinforcement input is more restrictive, False otherwise.
        """
        pass
