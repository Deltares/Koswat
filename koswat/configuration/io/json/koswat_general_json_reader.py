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

import math
from pathlib import Path

from koswat.configuration.io.json.koswat_general_json_fom import KoswatGeneralJsonFom
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatGeneralJsonReader(KoswatReaderProtocol):
    """
    Reader for the general KOSWAT JSON configuration files.
    It correctly sets its properties in case of special configurations, e.g. when waterside reinforcement is allowed but no ground price is provided.
    """

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".json"

    def read(self, from_path: Path) -> KoswatGeneralJsonFom:
        reader = KoswatJsonReader()
        _json_fom = reader.read(from_path)
        _imported_json = KoswatGeneralJsonFom.from_json(_json_fom)
        return self._normalize_imported_json(_imported_json)

    def _normalize_imported_json(
        self, _generated_object: KoswatGeneralJsonFom
    ) -> KoswatGeneralJsonFom:
        if (
            not _generated_object.surroundings_section.allow_waterside_reinforcement
            and (
                _generated_object.dike_profile_section.ground_price_waterside is None
                or math.isnan(
                    _generated_object.dike_profile_section.ground_price_waterside
                )
            )
        ):
            _generated_object.dike_profile_section.ground_price_waterside = 0.0
        return _generated_object
