import logging
from dataclasses import dataclass, field
from pathlib import Path

from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


@dataclass(kw_only=True)
class KoswatSectionScenarioListIniDirReader(KoswatReaderProtocol):
    dike_selection: list[str] = field(default_factory=list)

    def _selected_scenario(self, scenario_file: Path) -> bool:
        if not self.dike_selection:
            # All dikes selected.
            return True
        if scenario_file.stem not in self.dike_selection:
            logging.error(
                "Scenario %s skipped because section was not selected.",
                scenario_file.stem,
            )
            return False
        return True

    def _get_scenario(self, scenario_file: Path) -> KoswatSectionScenariosIniFom:
        _reader = KoswatIniReader()
        _reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
        _section_scenarios: KoswatSectionScenariosIniFom = _reader.read(scenario_file)
        _section_scenarios.scenario_dike_section = scenario_file.stem
        return _section_scenarios

    def read(self, dir_path: Path) -> list[KoswatSectionScenariosIniFom]:
        if not dir_path.is_dir():
            logging.error("Scenarios directory not found at %s", dir_path)
            return []

        return list(
            map(
                self._get_scenario,
                filter(self._selected_scenario, dir_path.glob("*.ini")),
            )
        )
