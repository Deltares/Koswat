import math
from dataclasses import dataclass

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureLocationCosts:
    location: PointSurroundings
    zone_a: float = math.nan
    zone_a_costs: float = math.nan

    zone_b: float = math.nan
    zone_b_costs: float = math.nan
    surtax_costs: float = math.nan


@dataclass
class InfrastructureProfileCostsCalculator:
    infrastructure: SurroundingsInfrastructure
    surtax_costs: float
    zone_a_costs: float
    zone_b_costs: float

    def calculate(
        self, zone_a_width: float, zone_b_width: float
    ) -> list[InfrastructureLocationCosts]:
        return (math.nan, math.nan)

    def _calculate_at_location(
        self, zone_a_width: float, zone_b_width: float, location: PointSurroundings
    ) -> InfrastructureLocationCosts:
        _total_zone_a = location.get_total_infrastructure_length(0, zone_a_width)
        _total_zone_b = location.get_total_infrastructure_length(
            zone_a_width, zone_b_width
        )
        return InfrastructureLocationCosts(
            location=location,
            surtax_costs=self.surtax_costs,
            zone_a=_total_zone_a * self.infrastructure.infrastructure_width,
            zone_b=_total_zone_b * self.infrastructure.infrastructure_width,
            zone_a_costs=_total_zone_a * self.zone_a_costs,
            zone_b_costs=_total_zone_b * self.zone_b_costs,
        )
