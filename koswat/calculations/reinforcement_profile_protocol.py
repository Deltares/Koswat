from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.calculations.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


@runtime_checkable
class ReinforcementProfileProtocol(KoswatProfileProtocol, Protocol):
    input_data: ReinforcementInputProfileProtocol
    layers_wrapper: ReinforcementLayersWrapper
