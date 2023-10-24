from typing import Protocol, runtime_checkable

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.core.protocols import BuilderProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


@runtime_checkable
class ReinforcementProfileBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: type[ReinforcementProfileProtocol]

    def build(self) -> ReinforcementProfileProtocol:
        """
        Builds a concrete instance of a `ReinforcementProfileProtocol` based on the required data.

        Returns:
            ReinforcementProfileProtocol: Valid instance of a `ReinforcementProfileProtocol`.
        """
        pass