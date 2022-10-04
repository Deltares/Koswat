from __future__ import annotations

from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_csv_reader import KoswatCsvFom
from koswat.io.koswat_shp_reader import KoswatShpFom
from koswat.surroundings.koswat_buildings_polderside import KoswatBuildingsPolderside


class KoswatBuildingsPoldersideBuilder(BuilderProtocol):
    koswat_shp_fom: KoswatShpFom = None
    koswat_csv_fom: KoswatCsvFom = None

    def build(self) -> KoswatBuildingsPolderside:
        if not self.koswat_shp_fom or not self.koswat_csv_fom:
            raise ValueError("FileObjectModel for both CSV and SHP should be provided.")

        return super().build()
