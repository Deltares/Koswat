import logging
from dataclasses import dataclass, field
from pathlib import Path

from koswat.configuration.io.json.koswat_section_scenario_json_fom import (
    KoswatSectionScenariosJsonFom,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


@dataclass(kw_only=True)
class KoswatSectionScenarioListJsonDirReader(KoswatReaderProtocol):
    dike_selection: list[str] = field(default_factory=list)

    def _selected_scenario(self, scenario_file: Path) -> bool:
        return scenario_file.stem in self.dike_selection

    def _get_scenario(self, scenario_file: Path) -> KoswatSectionScenariosJsonFom:
        _reader = KoswatJsonReader()
        _json_fom = _reader.read(scenario_file)
        _section_scenario = KoswatSectionScenariosJsonFom.from_config(_json_fom.content)
        _section_scenario.scenario_dike_section = _json_fom.file_stem
        return _section_scenario

    def read(self, dir_path: Path) -> list[KoswatSectionScenariosJsonFom]:
        if not dir_path.is_dir():
            logging.error("Scenarios directory not found at %s", dir_path)
            return []

        return list(
            map(
                self._get_scenario,
                filter(self._selected_scenario, dir_path.glob("*.json")),
            )
        )
