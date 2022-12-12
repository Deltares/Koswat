from typing import List

from koswat.configuration.koswat_scenario import KoswatScenario


class KoswatConfiguration:
    scenarios: List[KoswatScenario]
    dike_sections: List[str]

    def __init__(self) -> None:
        self.scenarios = []
        self.dike_sections = []

    def is_valid(self) -> bool:
        return any(self.scenarios) and all(_s.is_valid() for _s in self.scenarios) and any(self.dike_sections)

    def run(self) -> None:
        if not self.is_valid():
            return
