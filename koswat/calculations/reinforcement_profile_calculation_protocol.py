from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.koswat_scenario import KoswatScenario


@runtime_checkable
class ReinforcementProfileCalculationProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def build(self) -> ReinforcementProfileProtocol:
        pass
