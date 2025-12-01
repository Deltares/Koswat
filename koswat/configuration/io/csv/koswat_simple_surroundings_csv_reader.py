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

from shapely import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatSimpleSurroundingsCsvReader(KoswatReaderProtocol):
    """
    Imports surroundings expecting simplified format.
    
    E.g.:
        Sectie;Xcoord;Ycoord;dist_binnen;dist_buiten;angle_binnen;angle_buiten
        A;199186.66;515698.01;500;500;-76.0;104.0
    """
    def read(self, file_path: Path) -> KoswatSurroundingsCsvFom:
        _csv_fom = KoswatCsvReader().read(file_path)

        # First three columns are section, x and y coordinate.
        _koswat_fom = KoswatSurroundingsCsvFom()
        _koswat_fom.points_surroundings_list = self._build_points_surroundings_list(
           _csv_fom.entries
        )
        return _koswat_fom

    def _build_points_surroundings_list(
        self, entries: list[list[str]]
    ) -> list[PointSurroundings]:
        _point_list = []
        for idx, _point_entry in enumerate(entries):
            _point_entry.insert(0, idx)
            _ps = self._build_point_surroundings(_point_entry)
            _point_list.append(_ps)
        return _point_list

    def _build_point_surroundings(
        self, entry: list[str]
    ) -> PointSurroundings:
        return PointObstacleSurroundings(
            section=entry[1],
            traject_order=entry[0],
            location=Point(float(entry[2]), float(entry[3])),
            surroundings_matrix=[],
            inside_distance=float(entry[4]),
            outside_distance=float(entry[5]),
            angle_inside=float(entry[6]),
            angle_outside=float(entry[7]),
        )
