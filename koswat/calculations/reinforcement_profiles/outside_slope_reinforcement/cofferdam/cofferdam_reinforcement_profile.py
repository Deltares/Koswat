from koswat.calculations.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.calculations.reinforcement_profiles.outside_slope_reinforcement.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)


class CofferdamReinforcementProfile(OutsideSlopeReinforcementProfile):
    input_data: CofferDamInputProfile

    def __str__(self) -> str:
        return "Kistdam"
