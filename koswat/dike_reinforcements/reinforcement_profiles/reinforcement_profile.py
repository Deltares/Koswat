from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)

from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class ReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    input_data: ReinforcementInputProfileProtocol
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float

    @property
    def new_ground_level_surface(self) -> float:
        return self.profile_width - self.old_profile.profile_width
