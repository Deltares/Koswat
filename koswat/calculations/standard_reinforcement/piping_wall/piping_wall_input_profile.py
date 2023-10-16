from __future__ import annotations
from dataclasses import dataclass
import math

from koswat.calculations.protocols import ReinforcementInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class PipingWallInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    length_piping_wall: float = math.nan
