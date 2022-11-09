from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class CofferdamReinforcementProfile(
    OutsideSlopeReinforcementProfile, KoswatProfileBase
):
    input_data: CofferDamInputProfile

    def __str__(self) -> str:
        return "Kistdam"
