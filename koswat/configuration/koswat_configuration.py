from typing import List

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.models.koswat_costs import KoswatCosts
from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.configuration.models.koswat_general_settings import KoswatGeneralSettings
from koswat.configuration.models.koswat_scenario import KoswatScenario


class KoswatConfiguration(KoswatConfigProtocol):
    scenarios: List[KoswatScenario]
    dike_selection: KoswatDikeSelection
    costs: KoswatCosts
    general: KoswatGeneralSettings

    def __init__(self) -> None:
        self.scenarios = []
        self.dike_selection = None
        self.costs = None
        self.general = None

    def is_valid(self) -> bool:
        return (
            self.general
            and self.general.is_valid()
            and self.scenarios
            and any(self.scenarios)
            and all(_s.is_valid() for _s in self.scenarios)
            and self.dike_selection
            and self.dike_selection.is_valid()
            and self.costs
            and self.costs.is_valid()
        )

    def run(self) -> None:
        if not self.is_valid():
            return
