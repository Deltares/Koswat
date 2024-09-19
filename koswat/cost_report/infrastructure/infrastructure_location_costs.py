import math
from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureLocationCosts:
    """
    Simple data structure containing the results of the costs calculations
    for a given `ReinforcementProfileProtocol` profile.
    The values related to `zone_a` and `zone_b` are calculated in the
    `ProfileZoneCalculator`.
    """

    infrastructure: SurroundingsInfrastructure = None
    location: PointSurroundings = None
    zone_a: float = math.nan
    zone_a_costs: float = math.nan

    zone_b: float = math.nan
    zone_b_costs: float = math.nan
    surtax_costs: float = math.nan

    @property
    def total_cost(self) -> float:
        return self.zone_a_costs + self.zone_b_costs
