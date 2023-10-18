from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class CofferDamInputProfile(KoswatInputProfileBase, ReinforcementProfileProtocol):
    length_coffer_dam: float = math.nan
