import math
from dataclasses import dataclass

from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureCostsCalculator:
    infrastructure: SurroundingsInfrastructure
    removing_costs: float
    adding_costs: float
    # non_rising_dike_costs: float
    # surtax_costs: float
    zone_a_costs: float
    zone_b_costs: float

    def calculate(
        self, zone_a_width: float, zone_b_width: float
    ) -> tuple[float, float]:
        return (math.nan, math.nan)
