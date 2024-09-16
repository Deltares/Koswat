from dataclasses import dataclass

from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


@dataclass
class InfrastructureCostsCalculator:
    infrastructure: SurroundingsInfrastructure
    removing_costs: float
    adding_costs: float
    storage_costs: float
    non_rising_dike_costs: float
    surtax_costs: float

    def get_zone_a_costs(self, dike_profile) -> tuple[float, float]:
        # returns tuple:
        # - length of infrastructure in zone 'a'
        # - total cost
        pass

    def get_zone_b_costs(self, dike_profile) -> tuple[float, float]:
        # returns tuple:
        # - length of infrastructure in zone 'b'
        # - total cost
        pass
