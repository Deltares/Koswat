import logging
from pathlib import Path
from typing import List

from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class KoswatRunScenarioSettings:
    scenario: KoswatScenario
    surroundings: SurroundingsWrapper
    costs: KoswatCostsSettings
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


class KoswatRunSettings:
    run_scenarios: List[KoswatRunScenarioSettings]
    input_profile_cases: List[KoswatProfileBase]
    output_dir: Path

    def __init__(self) -> None:
        self.run_scenarios = []
        self.input_profile_cases = []
        self.output_dir = None

    def run(self) -> None:
        logging.info("Initializing run for all cases.")

        logging.info("Finalized run for all cases.")
