from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class StabilityWallReinforcementProfile(StandardReinforcementProfile):
    input_data: StabilityWallInputProfile

    def __str__(self) -> str:
        return "Stabiliteitswand"
