from dataclasses import dataclass

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
    infrastructure_calculators: list[InfrastructureProfileCostsCalculator]

    def calculate(
        self, reinforced_profile: ReinforcementProfileProtocol
    ) -> list[InfrastructureLocationProfileCostReport]:
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
                        infrastructure=_calculator.infrastructure,
                        infrastructure_location_costs=_subreport,
                    )
                    for _subreport in _subreports
                ]
            )

        return _reports
