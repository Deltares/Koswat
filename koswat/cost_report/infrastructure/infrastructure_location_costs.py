import math
from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureLocationCosts:
    infrastructure: SurroundingsInfrastructure = None
    location: PointSurroundings = None
    zone_a: float = math.nan
    zone_a_costs: float = math.nan

    zone_b: float = math.nan
    zone_b_costs: float = math.nan
    surtax_costs: float = math.nan
