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
