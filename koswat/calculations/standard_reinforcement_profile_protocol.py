from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@runtime_checkable
class StandardReinforcementProfileProtocol(ReinforcementProfileProtocol, Protocol):
    pass
