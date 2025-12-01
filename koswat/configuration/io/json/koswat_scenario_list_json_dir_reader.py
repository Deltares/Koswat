"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
