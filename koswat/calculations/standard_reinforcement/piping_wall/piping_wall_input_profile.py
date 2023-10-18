from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.calculations.protocols import ReinforcementInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class PipingWallInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    length_piping_wall: float = math.nan
