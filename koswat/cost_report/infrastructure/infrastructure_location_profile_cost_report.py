import math
from dataclasses import dataclass

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureLocationCosts,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class InfrastructureLocationProfileCostReport(CostReportProtocol):
    # Report classifiers.
    reinforced_profile: ReinforcementProfileProtocol
    infrastructure: SurroundingsInfrastructure

    # Report calculated properties.
    infrastructure_location_costs: InfrastructureLocationCosts

    @property
    def location(self) -> PointSurroundings:
        if not self.infrastructure_location_costs:
            return PointSurroundings()
        return self.infrastructure_location_costs.location

    @property
    def total_cost(self) -> float:
        if not self.infrastructure_location_costs:
            return math.nan
        return (
            self.infrastructure_location_costs.zone_a_costs
            + self.infrastructure_location_costs.zone_b_costs
        )

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.infrastructure_location_costs:
            return math.nan
        return self.total_cost * self.infrastructure_location_costs.surtax_costs
