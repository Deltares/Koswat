from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)


@dataclass
class StabilityWallInputProfile(
    KoswatInputProfileBase, ReinforcementInputProfileProtocol
):
    length_stability_wall: float = math.nan

    @property
    def reinforcement_domain_name(self) -> str:
        return "Stabiliteitswand"
