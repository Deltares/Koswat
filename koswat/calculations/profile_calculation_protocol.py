from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfile


@runtime_checkable
class ProfileCalculationProtocol(Protocol):
    def calculate_new_profile(
        self, profile: KoswatProfile, scenario: KoswatScenario
    ) -> KoswatProfile:
        pass
