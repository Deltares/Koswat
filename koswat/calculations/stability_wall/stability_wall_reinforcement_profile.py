from koswat.calculations.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class StabilityWallReinforcementProfile(
    StandardReinforcementProfileProtocol, KoswatProfileBase
):
    input_data: StabilityWallInputProfile

    def __str__(self) -> str:
        return "Stabiliteitswand"
