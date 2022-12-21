from __future__ import annotations

from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class CofferDamInputProfile(KoswatInputProfileBase, ReinforcementProfileProtocol):
    length_coffer_dam: float
