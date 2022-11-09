from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class SoilReinforcementProfile(StandardReinforcementProfile, KoswatProfileBase):
    def __str__(self) -> str:
        return "Grondmaatregel profiel"
