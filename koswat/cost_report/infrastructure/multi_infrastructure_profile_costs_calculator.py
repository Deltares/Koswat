from dataclasses import dataclass

from koswat.cost_report.infrastructure.infrastructure_costs_calculator import (
    InfrastructureCostsCalculator,
)
from koswat.cost_report.infrastructure.infrastructure_profile_cost_report import (
    InfrastructureProfileCostReport,
)
from koswat.cost_report.infrastructure.profile_zone_calculator import (
    ProfileZoneCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class MultiInfrastructureProfileCostsCalculator:
    infrastructure_calculators: dict[str, InfrastructureCostsCalculator]

    def calculate(
        self, reinforced_profile: ReinforcementProfileProtocol
    ) -> InfrastructureProfileCostReport:
        _length_zone_a, _length_zone_b = ProfileZoneCalculator(
            reinforced_profile=reinforced_profile
        ).calculate()

        _report = InfrastructureProfileCostReport(reinforced_profile=reinforced_profile)

        return _report
