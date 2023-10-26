from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class StabilityWallReinforcementProfile(StandardReinforcementProfile):
    output_name: str = "Stabiliteitswand"
    input_data: StabilityWallInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float

    def __str__(self) -> str:
        return self.output_name
