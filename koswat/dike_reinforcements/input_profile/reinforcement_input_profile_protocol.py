from typing import Protocol, runtime_checkable

from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@runtime_checkable
class ReinforcementInputProfileProtocol(KoswatInputProfileProtocol, Protocol):
    """
    Just an alias to distinguish from a regular `KoswatInputProfileProtocol`.
    """

    construction_length: float
    construction_type: ConstructionTypeEnum | None

    @property
    def reinforcement_domain_name(self) -> str:
        """
        Returns the representative name in the "real" world of this reinforcement.
        """
        pass
