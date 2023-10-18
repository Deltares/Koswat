from dataclasses import dataclass
from koswat.calculations.protocols import ReinforcementInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase

@dataclass
class SoilInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    pass
