from koswat.calculations.cofferdam.cofferdam_input_profile import CofferDamInputProfile
from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfileProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class CofferdamReinforcementProfile(
    OutsideSlopeReinforcementProfileProtocol, KoswatProfileBase
):
    input_data: CofferDamInputProfile

    def __str__(self) -> str:
        return "Kistdam"
