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

import math
from dataclasses import dataclass

from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureProfileCostsCalculator:
    """
    Calculator to generate all `InfrastructureLocationCosts` instances
    based on the locations of the contained infrastructure
    (`SurroundingsInfrastructure.points`) and the width of `zone_a` and
    `zone_b`.
    """

    infrastructure: SurroundingsInfrastructure = None
    surtax: float = math.nan
    zone_a_costs: float = 0.0
    zone_b_costs: float = 0.0

    def calculate(
        self, zone_a_width: float, zone_b_width: float
    ) -> list[InfrastructureLocationCosts]:
        """
        Calculates the costs affecting this instance's infrastructure
        at all points where it is present.

        Args:
            zone_a_width (float): Width of zone type `A`.
            zone_b_width (float): Width of zone type `B .

        Returns:
            list[InfrastructureLocationCosts]: Resulting cost summaries.
        """

        return [
            self._calculate_at_location(
                zone_a_width=zone_a_width,
                zone_b_width=zone_b_width,
                location=_location,
            )
            for _location in self.infrastructure.points
            if any(_location.surroundings_matrix.items())
        ]

    def _calculate_at_location(
        self, zone_a_width: float, zone_b_width: float, location: PointSurroundings
    ) -> InfrastructureLocationCosts:
        _zone_a_limits = (0, zone_a_width)
        _zone_b_limits = (zone_a_width, zone_a_width + zone_b_width)
        _total_zone_a, _total_zone_b = location.get_total_infrastructure_per_zone(
            _zone_a_limits, _zone_b_limits
        )

        _surface_zone_a = _total_zone_a * self.infrastructure.infrastructure_width
        _surface_zone_b = _total_zone_b * self.infrastructure.infrastructure_width

        return InfrastructureLocationCosts(
            location=location,
            surtax=self.surtax,
            zone_a=_surface_zone_a,
            zone_b=_surface_zone_b,
            zone_a_costs=_surface_zone_a * self.zone_a_costs,
            zone_b_costs=_surface_zone_b * self.zone_b_costs,
        )
