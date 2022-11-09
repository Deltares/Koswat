from typing import List, Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.soil.soil_reinforcement_profile import SoilReinforcementProfile
from koswat.calculations.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


class ReinforcementProfileCalculationFactoryBuilder(BuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[ReinforcementProfileProtocol]

    @staticmethod
    def get_available_reinforcements() -> List[ReinforcementProfileProtocol]:
        return [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    def build(self) -> ReinforcementProfileProtocol:
        if issubclass(self.reinforcement_profile_type, StandardReinforcementProfile):
            _builder = StandardReinforcementProfileBuilder()
            _builder.base_profile = self.base_profile
            _builder.scenario = self.scenario
            return _builder.build()
        elif issubclass(
            self.reinforcement_profile_type, OutsideSlopeReinforcementProfile
        ):
            _builder = OutsideSlopeReinforcementProfileBuilder()
            _builder.base_profile = self.base_profile
            _builder.scenario = self.scenario
            return _builder.build()
        else:
            raise NotImplementedError(
                f"Type {self.reinforcement_profile_type} not currently supported."
            )
