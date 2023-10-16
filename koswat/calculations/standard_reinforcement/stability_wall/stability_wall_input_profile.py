from __future__ import annotations
from dataclasses import dataclass
import math

from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class StabilityWallInputProfile(KoswatInputProfileBase, ReinforcementProfileProtocol):
    length_stability_wall: float = math.nan
