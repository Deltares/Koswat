from __future__ import annotations

from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_csv_reader import KoswatCsvFom
from koswat.io.koswat_shp_reader import KoswatShpFom
from koswat.surroundings.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)


class KoswatBuildingsPoldersideBuilder(BuilderProtocol):
    koswat_shp_fom: KoswatShpFom = None
    koswat_csv_fom: KoswatCsvFom = None

    def _find_conflicting_point_idx(self, limit_point: Point) -> int:
        for _ps_idx, ps in enumerate(self.koswat_csv_fom.points_surroundings_list):
            if limit_point.almost_equals(ps.location, 0.001):
                return _ps_idx
        raise ValueError(
            "No point fromt the *.shp file matches the ones in the *.csv file."
        )

    def _get_conflicting_points(
        self, start_idx: int, end_idx: int
    ) -> List[PointSurroundings]:
        if start_idx > end_idx:
            return self.koswat_csv_fom.points_surroundings_list[
                end_idx : (start_idx + 1)
            ]
        return self.koswat_csv_fom.points_surroundings_list[start_idx : (end_idx + 1)]

    def build(self) -> KoswatBuildingsPolderside:
        if not self.koswat_shp_fom or not self.koswat_csv_fom:
            raise ValueError("FileObjectModel for both CSV and SHP should be provided.")

        start_idx = self._find_conflicting_point_idx(self.koswat_shp_fom.initial_point)
        end_idx = self._find_conflicting_point_idx(self.koswat_shp_fom.end_point)
        _conflicting_points = self._get_conflicting_points(start_idx, end_idx)

        _kbp = KoswatBuildingsPolderside()
        _kbp.conflicting_points = [
            _cf for _cf in _conflicting_points if any(_cf.distance_to_buildings)
        ]

        return _kbp
