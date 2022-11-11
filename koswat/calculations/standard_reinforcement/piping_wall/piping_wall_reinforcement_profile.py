from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class PipingWallReinforcementProfile(StandardReinforcementProfile):
    input_data: PipingWallInputProfile

    def __str__(self) -> str:
        return "Kwelscherm"
