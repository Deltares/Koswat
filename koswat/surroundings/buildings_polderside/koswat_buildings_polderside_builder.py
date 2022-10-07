from __future__ import annotations

from pathlib import Path
from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_csv_reader import KoswatCsvFom, KoswatCsvReader
from koswat.io.koswat_shp_reader import KoswatShpFom, KoswatShpReader
from koswat.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)


class KoswatBuildingsPoldersideBuilder(BuilderProtocol):
    koswat_shp_fom: KoswatShpFom
    koswat_csv_fom: KoswatCsvFom

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

    @classmethod
    def from_files(
        cls, csv_file: Path, shp_file: Path
    ) -> KoswatBuildingsPoldersideBuilder:
        _builder = cls()
        _builder.koswat_csv_fom = KoswatCsvReader().read(csv_file)
        _builder.koswat_shp_fom = KoswatShpReader().read(shp_file)
        return _builder
