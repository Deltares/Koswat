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

from dataclasses import dataclass, field

from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.profile_zone_calculator import (
    ProfileZoneCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class MultiInfrastructureProfileCostsCalculator:
    """
    Calculator that contains all possible "infrastructure" calculators
    (`InfrastructureProfileCostsCalculator`) one for each of the available
    infrastructures in the current `KoswatScenario`.
    Its `calculate` method only requires a reinforcement
    (`ReinforcementProfileProtocol`) to determine all infrastructures' costs.
    """

    infrastructure_calculators: list[InfrastructureProfileCostsCalculator] = field(
        default_factory=lambda: []
    )

    def calculate(
        self, reinforced_profile: ReinforcementProfileProtocol
    ) -> list[InfrastructureLocationProfileCostReport]:
        """
        Calculates the costs related to appyling the provided `reinforcement_profile`
        at all the locations where an infrastructure is present. It first determines
        zone `A` and `B` and then provides their widths to the inner
        infrastructure calculators (`InfrastructureProfileCostsCalculator`).

        Args:
            reinforced_profile (ReinforcementProfileProtocol): Reinforcement to be applied.

        Returns:
            list[InfrastructureLocationProfileCostReport]: Collection of reports summarizing the cost-impact of a `reinforced_profile`.
        """
        _width_zone_a, _width_zone_b = ProfileZoneCalculator(
            reinforced_profile=reinforced_profile
        ).calculate()

        _reports = []
        for _calculator in self.infrastructure_calculators:
            _subreports = _calculator.calculate(_width_zone_a, _width_zone_b)
            _reports.extend(
                [
                    InfrastructureLocationProfileCostReport(
                        reinforced_profile=reinforced_profile,
                        infrastructure_name=_calculator.infrastructure.infrastructure_name,
                        infrastructure_location_costs=_subreport,
                    )
                    for _subreport in _subreports
                ]
            )

        return _reports
