"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatDikeSectionInputJsonFom,
)
from koswat.configuration.io.json.koswat_dike_section_input_json_reader import (
    KoswatDikeSectionInputJsonReader,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol


@dataclass(kw_only=True)
class KoswatDikeSectionInputListImporter(KoswatImporterProtocol):
    dike_selection: list[str] = field(default_factory=list)

    def import_from(self, from_path: Path) -> list[KoswatDikeSectionInputJsonFom]:
        _files = list(from_path.glob("*.json"))

        _section_input_list = []
        for _section in self.dike_selection if self.dike_selection else []:
            if _section not in (_file.stem for _file in _files):
                logging.error(
                    "The selected dike section %s was not found in the input profile files.",
                    _section,
                )

            _file = from_path.joinpath(f"{_section}.json")
            if not _file.exists():
                continue

            _section_input_list.append(KoswatDikeSectionInputJsonReader().read(_file))

        return _section_input_list
