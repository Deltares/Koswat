from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.koswat_scenario import KoswatScenario


class StabilityWallReinforcementProfileCalculation(ReinforcementProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def build(self) -> StabilityWallReinforcementProfile:
        return super().build()
