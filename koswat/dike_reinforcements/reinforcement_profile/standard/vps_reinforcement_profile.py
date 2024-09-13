from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.vertical_piping_solution.vps_input_profile import (
    VPSInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class VPSReinforcementProfile(StandardReinforcementProfile):
    output_name: str = "Verticale piping oplossing"
    input_data: VPSInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float
