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


class KoswatRunScenarioSettings(KoswatConfigProtocol):
    scenario: KoswatScenario
    reinforcement_settings: KoswatReinforcementSettings
    surroundings: SurroundingsWrapper
    costs_setting: KoswatCostsSettings
    output_dir: Path
    input_profile_case: KoswatProfileBase

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
