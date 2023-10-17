from __future__ import annotations

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
)
from koswat.dike.surroundings.railways_polderside.koswat_railways_polderside import (
    KoswatRailwaysPolderside,
)
from koswat.dike.surroundings.railways_polderside.koswat_railways_polderside_builder import (
    KoswatRailwaysPoldersideBuilder,
)
from koswat.dike.surroundings.waters_polderside.koswat_waters_polderside import (
    KoswatWatersPolderside,
)
from koswat.dike.surroundings.waters_polderside.koswat_waters_polderside_builder import (
    KoswatWatersPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class SurroundingsWrapperBuilder(BuilderProtocol):
    trajects_fom: KoswatDikeLocationsShpFom
    surroundings_fom: KoswatTrajectSurroundingsWrapperCsvFom

    def __init__(self) -> None:
        self.trajects_fom = None
        self.surroundings_fom = None

    def _get_buildings_polder_side(self) -> KoswatBuildingsPolderside:
        _builder = KoswatBuildingsPoldersideBuilder()
        _builder.koswat_shp_fom = self.trajects_fom
        _builder.koswat_csv_fom = self.surroundings_fom.buildings_polderside
        return _builder.build()
    
    def _get_railways_polder_side(self) -> KoswatRailwaysPolderside:
        _builder = KoswatRailwaysPoldersideBuilder()
        _builder.koswat_shp_fom = self.trajects_fom
        _builder.koswat_csv_fom = self.surroundings_fom.railways_polderside
        return _builder.build()
    
    def _get_waters_polder_side(self) -> KoswatWatersPolderside:
        _builder = KoswatWatersPoldersideBuilder()
        _builder.koswat_shp_fom = self.trajects_fom
        _builder.koswat_csv_fom = self.surroundings_fom.waters_polderside
        return _builder.build()

    def build(self) -> SurroundingsWrapper:
        if not isinstance(self.trajects_fom, KoswatDikeLocationsShpFom):
            raise ValueError("A KoswatDikeLocationShpFom needs to be specified.")
        if not isinstance(
            self.surroundings_fom, KoswatTrajectSurroundingsWrapperCsvFom
        ):
            raise ValueError(
                "A KoswatTrajectSurroundingsWrapperCsvFom needs to be specified."
            )

        _surroundings = SurroundingsWrapper()
        _surroundings.dike_section = self.trajects_fom.dike_section
        _surroundings.traject = self.trajects_fom.dike_traject
        _surroundings.subtraject = self.trajects_fom.dike_subtraject

        # For now we only include buildings_polderside/railway_polderside/water_polderside
        _surroundings.buildings_polderside = self._get_buildings_polder_side()
        _surroundings.railways_polderside = self._get_railways_polder_side()
        _surroundings.waters_polderside = self._get_waters_polder_side()

        return _surroundings
