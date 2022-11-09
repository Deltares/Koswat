from koswat.calculations.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class StabilityWallReinforcementProfile(
    StandardReinforcementProfile, KoswatProfileBase
):
    input_data: StabilityWallInputProfile

    def __str__(self) -> str:
        return "Stabiliteitswand"
