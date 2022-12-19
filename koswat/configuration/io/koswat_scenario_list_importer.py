import logging
from pathlib import Path
from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatScenarioListImporter(BuilderProtocol):
    scenario_dir: Path
    dike_selection: List[str]

    def __init__(self) -> None:
        self.scenario_dir = None
        self.dike_selection = []

    def _selected_scenario(self, scenario_file: Path) -> bool:
        if not self.dike_selection:
            # All dikes selected.
            return True
        if scenario_file.stem not in self.dike_selections:
            logging.error(
                "Scenario {} skipped because section was not selected.".format(
                    scenario_file.stem
                )
            )
            return False
        return True

    def _get_scenario(self, scenario_file: Path) -> KoswatSectionScenariosIniFom:
        _reader = KoswatIniReader()
        _reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
        _section_scenarios: KoswatSectionScenariosIniFom = _reader.read(scenario_file)
        _section_scenarios.scenario_section = scenario_file.stem
        return _section_scenarios

    def build(self) -> List[KoswatSectionScenariosIniFom]:
        if not self.scenario_dir.is_dir():
            logging.error(
                "Scenarios directory not found at {}".format(self.scenario_dir)
            )
            return []

        return list(
            map(
                self._get_scenario,
                filter(self._selected_scenario, self.scenario_dir.glob("*.ini")),
            )
        )
