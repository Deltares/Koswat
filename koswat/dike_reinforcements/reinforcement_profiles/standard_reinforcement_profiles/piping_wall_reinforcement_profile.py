from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.reinforcement_input_profiles.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profiles.standard_reinforcement_profiles.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class PipingWallReinforcementProfile(StandardReinforcementProfile):
    input_data: PipingWallInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float
