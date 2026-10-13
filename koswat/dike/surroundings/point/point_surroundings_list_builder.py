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

from dataclasses import dataclass

from shapely.geometry import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.shp import KoswatDikeLocationsShpFom
from koswat.core.protocols import BuilderProtocol

from .point_surroundings_protocol import PointSurroundingsProtocol


@dataclass
class PointSurroundingsListBuilder(BuilderProtocol):
    """
    Builds a collection of points (`list[PointSurroundingsProtocol]`) given the dike locations
    (`KoswatDikeLocationsShpFom`) and the surroundings around it
    (`KoswatSurroundingsCsvFom`).
    """

    koswat_shp_fom: KoswatDikeLocationsShpFom
    koswat_csv_fom: KoswatSurroundingsCsvFom

    def _find_point_idx(self, limit_point: Point) -> int:
        for _ps_idx, ps in enumerate(self.koswat_csv_fom.points_surroundings_list):
            if limit_point.equals_exact(ps.location, 0.5):
                return _ps_idx
        raise ValueError(
            "No point from the *.shp file matches the ones in the *.csv file."
        )

    def _get_traject_points(
        self, start_idx: int, end_idx: int
    ) -> list[PointSurroundingsProtocol]:
        if start_idx > end_idx:
            return self.koswat_csv_fom.points_surroundings_list[
                end_idx : (start_idx + 1)
            ]
        return self.koswat_csv_fom.points_surroundings_list[start_idx : (end_idx + 1)]

    def build(self) -> list[PointSurroundingsProtocol]:
        if not self.koswat_shp_fom or not self.koswat_csv_fom:
            raise ValueError("FileObjectModel for both CSV and SHP should be provided.")

        start_idx = self._find_point_idx(self.koswat_shp_fom.initial_point)
        end_idx = self._find_point_idx(self.koswat_shp_fom.end_point)

        return self._get_traject_points(start_idx, end_idx)
