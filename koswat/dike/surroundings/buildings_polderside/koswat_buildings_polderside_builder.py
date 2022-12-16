from __future__ import annotations

from pathlib import Path
from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom_builder import (
    KoswatSurroundingsCsvFomBuilder,
)
from koswat.configuration.io.shp import (
    KoswatDikeLocationsShpFom,
    KoswatDikeLocationsWrapperShpReader,
)
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.io.csv import KoswatCsvReader


class KoswatBuildingsPoldersideBuilder(BuilderProtocol):
    # TODO: this should probably be moved to configuration
    koswat_shp_fom: KoswatDikeLocationsShpFom
    koswat_csv_fom: KoswatTrajectSurroundingsCsvFom

    def __init__(self) -> None:
        self.koswat_csv_fom = None
        self.koswat_shp_fom = None

    def _find_polderside_point_idx(self, limit_point: Point) -> int:
        for _ps_idx, ps in enumerate(self.koswat_csv_fom.points_surroundings_list):
            if limit_point.almost_equals(ps.location, 0.001):
                return _ps_idx
        raise ValueError(
            "No point fromt the *.shp file matches the ones in the *.csv file."
        )

    def _get_polderside_points(
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

        start_idx = self._find_polderside_point_idx(self.koswat_shp_fom.initial_point)
        end_idx = self._find_polderside_point_idx(self.koswat_shp_fom.end_point)

        _kbp = KoswatBuildingsPolderside()
        _kbp.points = self._get_polderside_points(start_idx, end_idx)

        return _kbp
