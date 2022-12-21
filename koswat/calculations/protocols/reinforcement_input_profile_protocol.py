from typing import Protocol, runtime_checkable

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@runtime_checkable
class ReinforcementInputProfileProtocol(KoswatInputProfileProtocol, Protocol):
    """
    Just a wrapper (or alias) for the `ReinforcementProfileProtocol`
    """

    pass