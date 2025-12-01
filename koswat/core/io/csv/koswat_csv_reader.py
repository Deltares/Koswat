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

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatCsvReader(KoswatReaderProtocol):
    separator: str = ";"

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".csv"

    def read(self, file_path: Path) -> KoswatCsvFom:
        if not self.supports_file(file_path):
            raise ValueError("Csv file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _csv_lines = file_path.read_text().splitlines(keepends=False)
        _csv_entries = [_line.split(self.separator) for _line in _csv_lines]

        return KoswatCsvFom(headers=_csv_entries.pop(0), entries=_csv_entries)
