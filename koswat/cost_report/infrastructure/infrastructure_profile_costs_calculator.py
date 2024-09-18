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

    Returns:
        _type_: _description_
    """

    infrastructure: SurroundingsInfrastructure = None
    surtax_costs: float = math.nan
    zone_a_costs: float = math.nan
    zone_b_costs: float = math.nan

    def calculate(
        self, zone_a_width: float, zone_b_width: float
    ) -> list[InfrastructureLocationCosts]:
        """
        Calculates the costs affecting this instance's infrastructure
        at all points where its present.

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
        ]

    def _calculate_at_location(
        self, zone_a_width: float, zone_b_width: float, location: PointSurroundings
    ) -> InfrastructureLocationCosts:
        _zone_a_limits = (0, zone_a_width)
        _zone_b_limits = (zone_a_width, zone_a_width + zone_b_width)
        _total_zone_a, _total_zone_b = location.get_total_infrastructure_per_zone(
            _zone_a_limits, _zone_b_limits
        )

        return InfrastructureLocationCosts(
            infrastructure=self.infrastructure,
            location=location,
            surtax_costs=self.surtax_costs,
            zone_a=_total_zone_a * self.infrastructure.infrastructure_width,
            zone_b=_total_zone_b * self.infrastructure.infrastructure_width,
            zone_a_costs=_total_zone_a * self.zone_a_costs,
            zone_b_costs=_total_zone_b * self.zone_b_costs,
        )
