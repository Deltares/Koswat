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

from __future__ import annotations
from dataclasses import dataclass, field

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class KoswatSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: list[PointSurroundings] = field(
        default_factory=lambda: []
    )
    traject: str = ""

    def is_valid(self) -> bool:
        return any(self.points_surroundings_list)
    
    def merge(self, other: KoswatSurroundingsCsvFom) -> None:
        """
        Merge another KoswatSurroundingsCsvFom into this one.

        Args:
            other (KoswatSurroundingsCsvFom): The other KoswatSurroundingsCsvFom to merge.

        Raises:
            ValueError: If the trajects of the two objects do not match.
        """
        if other.traject != self.traject:
            raise ValueError("Cannot merge surroundings fom with different trajects.")

        # Note: Suboptimal, but sufficient for now.
        _as_dict = {point.location: point for point in self.points_surroundings_list}
        for point in other.points_surroundings_list:
            if point.location not in _as_dict:
                self.points_surroundings_list.append(point)
            else:
                _as_dict[point.location].merge(point)