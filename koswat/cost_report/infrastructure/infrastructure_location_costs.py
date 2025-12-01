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

import math
from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class InfrastructureLocationCosts:
    """
    Simple data structure containing the results of the costs calculations
    for a given `ReinforcementProfileProtocol` profile.
    The values related to `zone_a` and `zone_b` are calculated in the
    `ProfileZoneCalculator`.
    """

    location: PointSurroundings = None
    zone_a: float = 0.0
    zone_a_costs: float = 0.0

    zone_b: float = 0.0
    zone_b_costs: float = 0.0
    surtax: float = 0.0

    @property
    def total_cost(self) -> float:
        def valid_cost(cost: float) -> float:
            if math.isnan(cost):
                return 0
            return cost

        return valid_cost(self.zone_a_costs) + valid_cost(self.zone_b_costs)

    @property
    def total_cost_with_surtax(self) -> float:
        return self.total_cost * self.surtax
