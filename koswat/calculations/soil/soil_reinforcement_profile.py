from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class SoilReinforcementProfile(StandardReinforcementProfileProtocol, KoswatProfileBase):
    def __str__(self) -> str:
        return "Grondmaatregel profiel"
