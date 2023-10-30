from typing import Protocol, runtime_checkable

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@runtime_checkable
class ReinforcementInputProfileProtocol(KoswatInputProfileProtocol, Protocol):
    """
    Just an alias to distinguish from a regular `KoswatInputProfileProtocol`.
    """

    @property
    def reinforcement_domain_name(self) -> str:
        """
        Returns the representative name in the "real" world of this reinforcement.
        """
        pass

    @property
    def construction_length(self) -> float:
        """
        Returns the construction length of this reinforcement.
        """
