from __future__ import annotations

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
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
        _builder.koswat_csv_fom = self.surroundings_fom.buldings_polderside
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
        # For now we only include buildings_polderside
        _surroundings.buldings_polderside = self._get_buildings_polder_side()

        return _surroundings
