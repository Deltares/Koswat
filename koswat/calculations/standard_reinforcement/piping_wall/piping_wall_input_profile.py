from __future__ import annotations

from koswat.calculations.protocols import ReinforcementInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class PipingWallInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    length_piping_wall: float
