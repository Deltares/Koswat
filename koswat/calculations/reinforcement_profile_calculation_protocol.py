from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


@runtime_checkable
class ReinforcementProfileCalculationProtocol(Protocol):
    def calculate_new_profile(
        self, profile: KoswatProfileBase, scenario: KoswatScenario
    ) -> ReinforcementProfileProtocol:
        pass
