import logging
from pathlib import Path
from typing import List

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class KoswatRunSettings(KoswatConfigProtocol):
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
