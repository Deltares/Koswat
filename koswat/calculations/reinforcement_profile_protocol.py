from typing import Protocol, runtime_checkable

from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.calculations.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


@runtime_checkable
class ReinforcementProfileProtocol(KoswatProfileProtocol, Protocol):
    input_data: ReinforcementInputProfileProtocol
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float
