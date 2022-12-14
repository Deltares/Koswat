import logging
from pathlib import Path
from typing import List

from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.configuration.settings.koswat_scenario import KoswatScenario


class KoswatRunScenarioSettings:
    scenario: KoswatScenario
    costs: KoswatCostsSettings
    output_dir: Path

class KoswatRunSettings:
    run_scenarios: List[KoswatRunScenarioSettings]


    def run(self) -> None:
        logging.info("Initializing run for all cases.")

        logging.info("Finalized run for all cases.")
