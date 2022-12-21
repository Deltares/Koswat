from typing import Protocol, Type, runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.protocols.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.profile.koswat_profile import KoswatProfileBase


@runtime_checkable
class ReinforcementProfileBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[ReinforcementProfileProtocol]

    def build(self) -> ReinforcementProfileProtocol:
        """
        Builds a concrete instance of a `ReinforcementProfileProtocol` base don the required data.

        Returns:
            ReinforcementProfileProtocol: Valid instance of a `ReinforcementProfileProtocol`.
        """
        pass
