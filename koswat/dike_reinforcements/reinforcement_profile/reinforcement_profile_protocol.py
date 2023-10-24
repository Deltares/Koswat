from typing import Protocol, runtime_checkable

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)


@runtime_checkable
class ReinforcementProfileProtocol(KoswatProfileProtocol, Protocol):
    """
    Extension of the `KoswatProfileProtocol` to define the properties of a calculated reinforcement.
    """

    input_data: ReinforcementInputProfileProtocol
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float
