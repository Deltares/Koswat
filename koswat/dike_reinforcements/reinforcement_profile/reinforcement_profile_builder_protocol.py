from typing import Protocol, runtime_checkable

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@runtime_checkable
class ReinforcementProfileBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileBase
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario
    reinforcement_profile_type: type[ReinforcementProfileProtocol]

    def build(self) -> ReinforcementProfileProtocol:
        """
        Builds a concrete instance of a `ReinforcementProfileProtocol` based on the required data.

        Returns:
            ReinforcementProfileProtocol: Valid instance of a `ReinforcementProfileProtocol`.
        """
        pass
