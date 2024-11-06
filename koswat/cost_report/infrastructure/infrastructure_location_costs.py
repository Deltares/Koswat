from typing import TypedDict

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class InfrastructureLocationCosts(TypedDict):
    """
    Simple data structure containing the results of the costs calculations
    for a given `ReinforcementProfileProtocol` profile.
    The values related to `zone_a` and `zone_b` are calculated in the
    `ProfileZoneCalculator`.
    """

    location: PointSurroundings
    zone_a: float
    zone_a_costs: float

    zone_b: float
    zone_b_costs: float

    total_cost: float
    total_cost_with_surtax: float
