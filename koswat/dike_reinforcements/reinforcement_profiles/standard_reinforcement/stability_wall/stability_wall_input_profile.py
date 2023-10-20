from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass
class StabilityWallInputProfile(KoswatInputProfileBase, ReinforcementProfileProtocol):
    length_stability_wall: float = math.nan
