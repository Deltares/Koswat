from dataclasses import dataclass
from pathlib import Path

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


@dataclass
class KoswatRunScenarioSettings(KoswatConfigProtocol):
    scenario: KoswatScenario = None
    reinforcement_settings: KoswatReinforcementSettings = None
    surroundings: SurroundingsWrapper = None
    costs_setting: KoswatCostsSettings = None
    output_dir: Path = None
    input_profile_case: KoswatProfileBase = None

    @property
    def name(self) -> str:
        if not self.scenario:
            return ""
        return (
            self.scenario.scenario_name
            + "_"
            + self.scenario.scenario_section
            + "_"
            + self.input_profile_case.input_data.dike_section
        )
