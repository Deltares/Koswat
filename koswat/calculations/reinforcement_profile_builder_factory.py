from typing import List, Type

from koswat.calculations.outside_slope_reinforcement import (
    CofferDamInputProfile,
    CofferdamReinforcementProfile,
    OutsideSlopeReinforcementProfile,
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.calculations.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
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

_reinforcements = {
    SoilReinforcementProfile: SoilInputProfile,
    PipingWallReinforcementProfile: PipingWallInputProfile,
    StabilityWallReinforcementProfile: StabilityWallInputProfile,
    CofferdamReinforcementProfile: CofferDamInputProfile,
}


class ReinforcementProfileBuilderFactory:
    @staticmethod
    def get_available_reinforcements() -> List[ReinforcementProfileProtocol]:
        return list(_reinforcements.keys())

    @staticmethod
    def get_reinforcement_input_profile(
        reinforcement_profile: ReinforcementProfileProtocol,
    ) -> ReinforcementInputProfileProtocol:
        _input_profile = _reinforcements.get(reinforcement_profile, None)
        if not _input_profile:
            raise NotImplementedError(
                "Reinforcement profile {} not recognized.".format(reinforcement_profile)
            )
        return _input_profile

    @staticmethod
    def get_builder(
        reinforcement_profile_type: Type[ReinforcementProfileProtocol],
    ) -> ReinforcementProfileBuilderProtocol:
        if issubclass(reinforcement_profile_type, StandardReinforcementProfile):
            _builder = StandardReinforcementProfileBuilder()
            _builder.reinforcement_profile_type = reinforcement_profile_type
            return _builder
        elif issubclass(reinforcement_profile_type, OutsideSlopeReinforcementProfile):
            _builder = OutsideSlopeReinforcementProfileBuilder()
            _builder.reinforcement_profile_type = reinforcement_profile_type
            return _builder
        else:
            raise NotImplementedError(
                f"Type {reinforcement_profile_type} not currently supported."
            )
