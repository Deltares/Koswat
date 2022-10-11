from koswat.calculations.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class PipingWallReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    input_data: PipingWallInputProfile

    def __str__(self) -> str:
        return "Kwelscherm"
