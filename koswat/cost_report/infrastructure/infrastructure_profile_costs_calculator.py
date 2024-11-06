import math
from dataclasses import dataclass

from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureProfileCostsCalculator:
    """
    Calculator to generate all `InfrastructureLocationCosts` instances
    based on the locations of the contained infrastructure
    (`SurroundingsInfrastructure.points`) and the width of `zone_a` and
    `zone_b`.
    """

    infrastructure: SurroundingsInfrastructure = None
    surtax: float = math.nan
    zone_a_costs: float = 0
    zone_b_costs: float = 0

    def calculate(
        self, zone_a_width: float, zone_b_width: float
    ) -> list[InfrastructureLocationCosts]:
        """
        Calculates the costs affecting this instance's infrastructure
        at all points where it is present.

        Args:
            zone_a_width (float): Width of zone type `A`.
            zone_b_width (float): Width of zone type `B .

        Returns:
            list[InfrastructureLocationCosts]: Resulting cost summaries.
        """

        return [
            self._calculate_at_location(
                zone_a_width=zone_a_width,
                zone_b_width=zone_b_width,
                location=_location,
            )
            for _location in self.infrastructure.points
            if any(_location.surroundings_matrix.items())
        ]

    def _calculate_at_location(
        self, zone_a_width: float, zone_b_width: float, location: PointSurroundings
    ) -> InfrastructureLocationCosts:
        _zone_a_limits = (0, zone_a_width)
        _zone_b_limits = (zone_a_width, zone_a_width + zone_b_width)
        _total_zone_a, _total_zone_b = location.get_total_infrastructure_per_zone(
            _zone_a_limits, _zone_b_limits
        )

        _surface_zone_a = _total_zone_a * self.infrastructure.infrastructure_width
        _surface_zone_b = _total_zone_b * self.infrastructure.infrastructure_width

        def valid_cost(cost: float) -> float:
            if math.isnan(cost):
                return 0
            return cost

        _zone_a_cost = _surface_zone_a * self.zone_a_costs
        _zone_b_cost = _surface_zone_b * self.zone_b_costs
        _total_cost = valid_cost(_zone_a_cost) + valid_cost(_zone_b_cost)

        return InfrastructureLocationCosts(
            location=location,
            zone_a=_surface_zone_a,
            zone_b=_surface_zone_b,
            zone_a_costs=_zone_a_cost,
            zone_b_costs=_zone_b_cost,
            total_cost=_total_cost,
            total_cost_with_surtax=_total_cost * self.surtax,
        )
