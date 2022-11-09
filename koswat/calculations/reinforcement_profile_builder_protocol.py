from typing import Protocol, Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


class ReinforcementProfileBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[ReinforcementProfileProtocol]

    def build(self) -> ReinforcementProfileProtocol:
        pass