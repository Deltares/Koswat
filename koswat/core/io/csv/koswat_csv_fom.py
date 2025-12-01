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

from dataclasses import dataclass, field

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@dataclass
class KoswatCsvFom(KoswatCsvFomProtocol):
    headers: list[str] = field(default_factory=list)
    entries: list[list[str]] = field(default_factory=list)

    def is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)

        # At the moment, not all rows have the same length
        return all(map(lambda x: len(x) >= _l_header, self.entries))
