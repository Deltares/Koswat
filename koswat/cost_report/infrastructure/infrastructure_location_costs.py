import math
from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class InfrastructureLocationCosts:
    location: PointSurroundings
    zone_a: float = math.nan
    zone_a_costs: float = math.nan

    zone_b: float = math.nan
    zone_b_costs: float = math.nan
    surtax_costs: float = math.nan
