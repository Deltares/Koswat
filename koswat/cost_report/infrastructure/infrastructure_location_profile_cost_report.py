import math
from dataclasses import dataclass

from shapely import Point

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureLocationCosts,
)
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
    def location(self) -> Point:
        if not self.infrastructure_location_costs:
            return None
        return self.infrastructure_location_costs.location.location

    @property
    def total_cost(self) -> float:
        return math.nan

    @property
    def total_cost_with_surtax(self) -> float:
        return math.nan
