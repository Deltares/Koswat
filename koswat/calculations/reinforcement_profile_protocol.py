from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


@runtime_checkable
class ReinforcementProfileProtocol(KoswatProfileProtocol, Protocol):
    reinforcement_subtype: str
