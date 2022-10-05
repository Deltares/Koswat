from koswat.builder_protocol import BuilderProtocol
from koswat.koswat_report import MultipleProfileCostReport
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings
    base_profile: KoswatProfile
    scenario: KoswatScenario

    def build(self) -> MultipleProfileCostReport:
        return super().build()
