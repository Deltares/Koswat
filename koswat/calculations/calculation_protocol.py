from typing import Protocol

from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfile


class CalculationProtocol(Protocol):
    def calculate_new_geometry(
        profile: KoswatProfile, scenario: KoswatScenario
    ) -> KoswatProfile:
        pass
