from pathlib import Path
from typing import List

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)


class KoswatRunSettings(KoswatConfigProtocol):
    run_scenarios: List[KoswatRunScenarioSettings]
    output_dir: Path

    def __init__(self) -> None:
        self.run_scenarios = []
        self.output_dir = None