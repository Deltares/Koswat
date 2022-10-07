from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


@runtime_checkable
class ProfileCalculationProtocol(Protocol):
    def calculate_new_profile(
        self, profile: KoswatProfileBase, scenario: KoswatScenario
    ) -> KoswatProfileBase:
        pass
