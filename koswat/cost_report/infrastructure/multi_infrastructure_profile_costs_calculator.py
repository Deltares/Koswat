from dataclasses import dataclass

from koswat.cost_report.infrastructure.infrastructure_costs_calculator import (
    InfrastructureCostsCalculator,
)
from koswat.cost_report.infrastructure.infrastructure_profile_cost_report import (
    InfrastructureProfileCostReport,
)


@dataclass
class MultiInfrastructureProfileCostsCalculator:
    infrastructure_calculators: dict[str, InfrastructureCostsCalculator]

    def calculate(self, profile) -> InfrastructureProfileCostReport:
        _report = InfrastructureProfileCostReport(reinforced_profile=profile)
