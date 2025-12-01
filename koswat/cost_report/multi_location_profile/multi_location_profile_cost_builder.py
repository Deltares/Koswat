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

from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator_builder import (
    MultiInfrastructureProfileCostsCalculatorBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report_builder import (
    ProfileCostReportBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class MultiLocationProfileCostReportBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper = None
    reinforced_profile: ReinforcementProfileProtocol = None
    koswat_costs_settings: KoswatCostsSettings = None

    def build(self) -> MultiLocationProfileCostReport:

        # Profile cost report builder
        _profile_cost_report_builder = ProfileCostReportBuilder(
            reinforced_profile=self.reinforced_profile,
            koswat_costs_settings=self.koswat_costs_settings,
        )

        _infra_calculator = MultiInfrastructureProfileCostsCalculatorBuilder(
            infrastructure_wrapper=self.surroundings.infrastructure_surroundings_wrapper,
            cost_settings=self.koswat_costs_settings.infrastructure_costs,
            surtax_cost_settings=self.koswat_costs_settings.surtax_costs,
        ).build()

        # Multi-location profile cost report
        return MultiLocationProfileCostReport(
            report_locations=self.surroundings.get_locations_at_safe_distance(
                self.reinforced_profile.profile_width
            ),
            profile_cost_report=_profile_cost_report_builder.build(),
            infra_multilocation_profile_cost_report=_infra_calculator.calculate(
                self.reinforced_profile
            ),
        )
