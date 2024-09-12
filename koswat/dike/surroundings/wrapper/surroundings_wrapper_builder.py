from __future__ import annotations

from dataclasses import dataclass

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_list_polderside_builder import (
    PointSurroundingsListPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


@dataclass
class SurroundingsWrapperBuilder(BuilderProtocol):
    """
    Dataclass to wrapp all required properties to generate a `Surroundings` instance.
    """

    trajects_fom: KoswatDikeLocationsShpFom
    surroundings_fom: KoswatTrajectSurroundingsWrapperCsvFom
    surroundings_section: SurroundingsSectionFom

    def _get_polderside_surroundings_from_fom(
        self, csv_fom: KoswatTrajectSurroundingsWrapperCsvFom
    ) -> list[PointSurroundings]:
        _builder = PointSurroundingsListPoldersideBuilder(
            koswat_shp_fom=self.trajects_fom,
            koswat_csv_fom=csv_fom,
        )
        if not _builder.koswat_csv_fom:
            return []
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

        _surroundings = SurroundingsWrapper(
            dike_section=self.trajects_fom.dike_section,
            traject=self.trajects_fom.dike_traject,
            subtraject=self.trajects_fom.dike_subtraject,
            reinforcement_min_separation=self.surroundings_section.constructieafstand,
            reinforcement_min_buffer=self.surroundings_section.constructieovergang,
            apply_waterside=self.surroundings_section.buitendijks,
            apply_buildings=self.surroundings_section.bebouwing,
            apply_railways=self.surroundings_section.spoorwegen,
            apply_waters=self.surroundings_section.water,
        )

        # For now we only include:
        # buildings_polderside (mandatory)
        _surroundings.buildings_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.buildings_polderside
            )
        )
        if not _surroundings.buildings_polderside:
            raise ValueError(
                "Building surroundings CSV not provided or well formatted."
            )

        # railway_polderside (optional)
        _surroundings.railways_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.railways_polderside
            )
        )

        # water_polderside (optional)
        _surroundings.waters_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.waters_polderside
            )
        )

        # roads (optional)
        _surroundings.roads_class_2_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.roads_class_2_polderside
            )
        )
        _surroundings.roads_class_7_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.roads_class_7_polderside
            )
        )

        _surroundings.roads_class_24_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.roads_class_24_polderside
            )
        )
        _surroundings.roads_class_47_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.roads_class_47_polderside
            )
        )
        _surroundings.roads_class_unknown_polderside.points = (
            self._get_polderside_surroundings_from_fom(
                self.surroundings_fom.roads_class_unknown_polderside
            )
        )

        return _surroundings
