from koswat.calculations.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class PipingWallReinforcementProfile(StandardReinforcementProfile, KoswatProfileBase):
    input_data: PipingWallInputProfile

    def __str__(self) -> str:
        return "Kwelscherm"
