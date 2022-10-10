from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.calculations.cofferdam.cofferdam_input_profile import CofferDamInputProfile


class CofferdamReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    input_data: CofferDamInputProfile

    def __str__(self) -> str:
        return "Kistdam"
