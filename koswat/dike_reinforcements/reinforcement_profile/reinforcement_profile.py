from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class ReinforcementProfile(ReinforcementProfileProtocol, KoswatProfileBase):
    output_name: str
    input_data: ReinforcementInputProfileProtocol
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol

    @property
    def new_ground_level_surface(self) -> float:
        return self.profile_width - self.old_profile.profile_width

    def __str__(self) -> str:
        return self.output_name.replace(" ", "_")
