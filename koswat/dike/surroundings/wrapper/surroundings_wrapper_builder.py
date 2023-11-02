from __future__ import annotations

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
)
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside_builder import (
    KoswatSurroundingsPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class SurroundingsWrapperBuilder(BuilderProtocol):
    trajects_fom: KoswatDikeLocationsShpFom
    surroundings_fom: KoswatTrajectSurroundingsWrapperCsvFom
    surroundings_section: SurroundingsSectionFom

    def __init__(self) -> None:
        self.trajects_fom = None
        self.surroundings_fom = None
        self.surroundings_section = None

    def _get_surroundings_from_fom(
        self, csv_fom: KoswatTrajectSurroundingsWrapperCsvFom
    ) -> KoswatSurroundingsPolderside | None:
        _builder = KoswatSurroundingsPoldersideBuilder()
        _builder.koswat_shp_fom = self.trajects_fom
        _builder.koswat_csv_fom = csv_fom
        if not _builder.koswat_csv_fom:
            return None
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

        _surroundings.reinforcement_min_separation = (
            self.surroundings_section.constructieafstand
        )
        _surroundings.reinforcement_min_buffer = (
            self.surroundings_section.constructieovergang
        )

        _surroundings.apply_waterside = self.surroundings_section.buitendijks
        _surroundings.apply_buildings = self.surroundings_section.bebouwing
        _surroundings.apply_railways = self.surroundings_section.spoorwegen
        _surroundings.apply_waters = self.surroundings_section.water

        # For now we only include buildings_polderside(mandatory)/railway_polderside(optional)/water_polderside(optional)
        _surroundings.buildings_polderside = self._get_surroundings_from_fom(
            self.surroundings_fom.buildings_polderside
        )
        if not _surroundings.buildings_polderside:
            raise ValueError(
                "Building surroundings CSV not provided or formatted well."
            )
        _surroundings.railways_polderside = self._get_surroundings_from_fom(
            self.surroundings_fom.railways_polderside
        )
        _surroundings.waters_polderside = self._get_surroundings_from_fom(
            self.surroundings_fom.waters_polderside
        )

        return _surroundings
