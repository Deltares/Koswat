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

from dataclasses import dataclass

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class InfrastructureLocationProfileCostReport(CostReportProtocol):
    # Report classifiers.
    reinforced_profile: ReinforcementProfileProtocol
    infrastructure_name: str

    # Report calculated properties.
    infrastructure_location_costs: InfrastructureLocationCosts

    @property
    def location(self) -> PointSurroundings | None:
        if not self.infrastructure_location_costs:
            return None
        return self.infrastructure_location_costs.location

    @property
    def total_cost(self) -> float:
        if not self.infrastructure_location_costs:
            return 0.0
        return self.infrastructure_location_costs.total_cost

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.infrastructure_location_costs:
            return 0.0
        return self.total_cost * self.infrastructure_location_costs.surtax
