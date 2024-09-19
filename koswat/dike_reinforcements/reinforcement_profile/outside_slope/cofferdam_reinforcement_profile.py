from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)


class CofferdamReinforcementProfile(OutsideSlopeReinforcementProfile):
    output_name: str = "Kistdam"
    input_data: CofferDamInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float

    def __str__(self) -> str:
        return self.output_name
