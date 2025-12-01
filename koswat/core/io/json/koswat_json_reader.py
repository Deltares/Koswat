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

import json
from pathlib import Path

from koswat.core.io.json.koswat_json_fom import KoswatJsonFom
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatJsonReader(KoswatReaderProtocol):
    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".json"

    def read(self, file_path: Path) -> KoswatJsonFom:
        if not self.supports_file(file_path):
            raise ValueError("Json file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        with open(file_path, "r", encoding="utf-8") as _file:
            _json_content = json.load(_file)

        def _normalize_keys(_json_content: dict) -> dict:
            # All keys to lowercase
            return {
                k.lower(): _normalize_keys(v) if isinstance(v, dict) else v
                for k, v in _json_content.items()
            }

        return KoswatJsonFom(
            file_path=file_path, content=_normalize_keys(_json_content)
        )
