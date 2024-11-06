from typing import TypedDict

from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class InfrastructureLocationProfileCostReport(TypedDict):
    total_cost: float
    total_cost_with_surtax: float
    location: PointSurroundings | None

    # Report classifiers.
    reinforced_profile: ReinforcementProfileProtocol
    infrastructure_name: str

    # Report calculated properties.
    infrastructure_location_costs: InfrastructureLocationCosts
