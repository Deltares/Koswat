import math
from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class InfrastructureLocationCosts:
    """
    Simple data structure containing the results of the costs calculations
    for a given `ReinforcementProfileProtocol` profile.
    The values related to `zone_a` and `zone_b` are calculated in the
    `ProfileZoneCalculator`.
    """

    location: PointSurroundings = None
    zone_a: float = 0
    zone_a_costs: float = 0

    zone_b: float = 0
    zone_b_costs: float = 0
    surtax: float = 0

    @property
    def total_cost(self) -> float:
        def valid_cost(cost: float) -> float:
            if math.isnan(cost):
                return 0
            return cost

        return valid_cost(self.zone_a_costs) + valid_cost(self.zone_b_costs)
