from koswat.calculations.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class PipingWallReinforcementProfile(
    StandardReinforcementProfileProtocol, KoswatProfileBase
):
    input_data: PipingWallInputProfile

    def __str__(self) -> str:
        return "Kwelscherm"
