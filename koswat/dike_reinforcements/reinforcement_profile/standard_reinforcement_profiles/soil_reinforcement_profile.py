from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.standard_reinforcement_profiles.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class SoilReinforcementProfile(StandardReinforcementProfile):
    input_data: SoilInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float
