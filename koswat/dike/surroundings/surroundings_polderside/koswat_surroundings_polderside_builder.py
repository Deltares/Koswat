from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.configuration.io.shp import KoswatDikeLocationsShpFom
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class KoswatPointSurroundingsPoldersideBuilder(BuilderProtocol):
    koswat_shp_fom: KoswatDikeLocationsShpFom
    koswat_csv_fom: KoswatTrajectSurroundingsCsvFom

    def _find_polderside_point_idx(self, limit_point: Point) -> int:
        for _ps_idx, ps in enumerate(self.koswat_csv_fom.points_surroundings_list):
            if limit_point.almost_equals(ps.location, 0.001):
                return _ps_idx
        raise ValueError(
            "No point fromt the *.shp file matches the ones in the *.csv file."
        )

    def _get_polderside_points(
        self, start_idx: int, end_idx: int
    ) -> list[PointSurroundings]:
        if start_idx > end_idx:
            return self.koswat_csv_fom.points_surroundings_list[
                end_idx : (start_idx + 1)
            ]
        return self.koswat_csv_fom.points_surroundings_list[start_idx : (end_idx + 1)]

    def build(self) -> list[PointSurroundings]:
        if not self.koswat_shp_fom or not self.koswat_csv_fom:
            raise ValueError("FileObjectModel for both CSV and SHP should be provided.")

        start_idx = self._find_polderside_point_idx(self.koswat_shp_fom.initial_point)
        end_idx = self._find_polderside_point_idx(self.koswat_shp_fom.end_point)

        return self._get_polderside_points(start_idx, end_idx)
