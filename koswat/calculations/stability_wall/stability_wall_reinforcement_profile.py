from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class StabilityWallReinforcementProfile(
    ReinforcementProfileProtocol, KoswatProfileBase
):
    input_data: StabilityWallInputProfile

    def __str__(self) -> str:
        return "Stabiliteitswand"
