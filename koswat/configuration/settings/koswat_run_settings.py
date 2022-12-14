import logging
from pathlib import Path
from typing import List

from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class KoswatRunSettings:
    costs: KoswatCostsSettings
    input_profiles: List[KoswatProfileBase]
    scenarios: List[KoswatScenario]
    dike_sections: List[str]
    surroundings: List[Path]
    output_dir: Path

    def run(self) -> None:
        logging.info("Initializing run for all cases.")

        logging.info("Finalized run for all cases.")
