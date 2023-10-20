from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class SoilInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    pass
