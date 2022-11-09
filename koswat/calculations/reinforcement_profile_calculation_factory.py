from typing import List, Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)


class ReinforcementProfileCalculationFactory:
    @staticmethod
    def get_available_reinforcements() -> List[ReinforcementProfileProtocol]:
        return [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    @staticmethod
    def get_builder(
        reinforcement_profile_type: Type[ReinforcementProfileProtocol],
    ) -> ReinforcementProfileBuilderProtocol:
        if issubclass(reinforcement_profile_type, StandardReinforcementProfile):
            _builder = StandardReinforcementProfileBuilder()
            _builder.reinforcement_profile_type
            return _builder
        elif issubclass(reinforcement_profile_type, OutsideSlopeReinforcementProfile):
            _builder = OutsideSlopeReinforcementProfileBuilder()
            _builder.reinforcement_profile_type
            return _builder
        else:
            raise NotImplementedError(
                f"Type {reinforcement_profile_type} not currently supported."
            )
