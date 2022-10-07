from typing import Protocol

from typing_extensions import runtime_checkable

from koswat.koswat_scenario import KoswatScenario
from koswat.dike.koswat_profile import KoswatProfileBase


@runtime_checkable
class ProfileCalculationProtocol(Protocol):
    def calculate_new_profile(
        self, profile: KoswatProfileBase, scenario: KoswatScenario
    ) -> KoswatProfileBase:
        pass
