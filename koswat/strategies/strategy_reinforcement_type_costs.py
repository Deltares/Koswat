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

from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementTypeCosts:
    reinforcement_type: type[ReinforcementProfileProtocol]
    active: bool = True
    base_costs_with_surtax: float = 0.0
    infrastructure_costs: float = 0.0
    infrastructure_costs_with_surtax: float = 0.0

    @property
    def total_costs_with_surtax(self) -> float:
        """
        The simple addition of the base costs and the possible
        related infrastructure costs, both including surtax.

        Returns:
            float: The total costs with surtax when applying this reinforcement.
        """
        return self.base_costs_with_surtax + self.infrastructure_costs_with_surtax
