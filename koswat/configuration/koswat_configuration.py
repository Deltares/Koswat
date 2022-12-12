from typing import List

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_costs import KoswatCosts
from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.configuration.models.koswat_scenario import KoswatScenario


class KoswatConfiguration(KoswatConfigProtocol):
    scenarios: List[KoswatScenario]
    dike_sections: KoswatDikeSelection
    costs: KoswatCosts

    def __init__(self) -> None:
        self.scenarios = []
        self.dike_sections = None
        self.costs = None

    def is_valid(self) -> bool:
        return (
            any(self.scenarios)
            and all(_s.is_valid() for _s in self.scenarios)
            and self.dike_sections
            and self.dike_sections.is_valid()
            and self.costs
            and self.costs.is_valid()
        )

    def run(self) -> None:
        if not self.is_valid():
            return
