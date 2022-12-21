import logging
from pathlib import Path
from typing import List

from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatSectionScenarioListIniDirReader(KoswatReaderProtocol):
    dike_selection: List[str]

    def __init__(self) -> None:
        self.dike_selection = []

    def _selected_scenario(self, scenario_file: Path) -> bool:
        if not self.dike_selection:
            # All dikes selected.
            return True
        if scenario_file.stem not in self.dike_selection:
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

    def read(self, dir_path: Path) -> List[KoswatSectionScenariosIniFom]:
        if not dir_path.is_dir():
            logging.error(
                "Scenarios directory not found at {}".format(dir_path)
            )
            return []

        return list(
            map(
                self._get_scenario,
                filter(self._selected_scenario, dir_path.glob("*.ini")),
            )
        )
