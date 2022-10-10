from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class CofferdamReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    def __str__(self) -> str:
        return "Kistdam"
