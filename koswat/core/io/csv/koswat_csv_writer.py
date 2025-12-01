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

from pathlib import Path
from typing import List

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.core.io.koswat_writer_protocol import KoswatWriterProtocol


class KoswatCsvWriter(KoswatWriterProtocol):
    separator: str = ";"

    def write(self, fom_instance: KoswatCsvFomProtocol, to_path: Path) -> None:
        if not isinstance(fom_instance, KoswatCsvFomProtocol):
            raise ValueError("Expected instance of type 'KoswatCsvFomProtocol'.")
        if not isinstance(to_path, Path):
            raise ValueError("No write path location provided.")

        def format_line(line: List[str]) -> str:
            return ";".join(map(str, line))

        _headers = (
            fom_instance.headers
            if isinstance(fom_instance.headers[0], list)
            else [fom_instance.headers]
        )

        _lines = list(map(format_line, _headers + fom_instance.entries))
        _text = "\n".join(_lines)

        to_path.write_text(_text)
