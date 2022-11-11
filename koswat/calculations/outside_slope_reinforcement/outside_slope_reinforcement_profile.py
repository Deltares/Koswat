from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class OutsideSlopeReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    @property
    def new_ground_level_surface(self) -> float:
        return self.profile_width - self.old_profile.profile_width
