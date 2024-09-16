import logging
from dataclasses import dataclass, field
from itertools import groupby
from pathlib import Path

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_reader import (
    KoswatSurroundingsCsvReader,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsListShpReader,
)
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_list_polderside_builder import (
    PointSurroundingsListPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


@dataclass
class SurroundingsWrapperBuilder(BuilderProtocol):
    surroundings_section_fom: SurroundingsSectionFom
    infrastructure_section_fom: InfrastructureSectionFom
    location_shp_fom: KoswatDikeLocationsShpFom
    surroundings_csv_fom_collection: dict[str, KoswatSurroundingsCsvFom]

    def build(self) -> SurroundingsWrapper:
        return SurroundingsWrapper(
            dike_section=self.location_shp_fom.dike_section,
            traject=self.location_shp_fom.dike_traject,
            subtraject=self.location_shp_fom.dike_subtraject,
            obstacle_surroundings_wrapper=self._get_obstacle_surroundings_wrapper(),
            infrastructure_surroundings_wrapper=self._get_infrastructure_surroundings_wrapper(),
        )

    def _get_polderside_surroundings_from_fom(
        self, csv_fom_name: str
    ) -> list[PointSurroundings]:
        _builder = PointSurroundingsListPoldersideBuilder(
            koswat_shp_fom=self.location_shp_fom,
            koswat_csv_fom=self.surroundings_csv_fom_collection[csv_fom_name],
        )
        if not _builder.koswat_csv_fom:
            return []
        return _builder.build()

    def _get_obstacle_surroundings_wrapper(self) -> ObstacleSurroundingsWrapper:
        _obs_wrapper = ObstacleSurroundingsWrapper(
            reinforcement_min_separation=self.surroundings_section_fom.constructieafstand,
            reinforcement_min_buffer=self.surroundings_section_fom.constructieovergang,
            apply_waterside=self.surroundings_section_fom.buitendijks,
            apply_buildings=self.surroundings_section_fom.bebouwing,
            apply_railways=self.surroundings_section_fom.spoorwegen,
            apply_waters=self.surroundings_section_fom.water,
        )
        _obs_wrapper.buildings_polderside.points = (
            self._get_polderside_surroundings_from_fom("buildings_polderside")
        )
        _obs_wrapper.railways_polderside.points = (
            self._get_polderside_surroundings_from_fom("railways_polderside")
        )
        _obs_wrapper.waters_polderside.points = (
            self._get_polderside_surroundings_from_fom("waters_polderside")
        )

        return _obs_wrapper

    def _get_infrastructure_surroundings_wrapper(
        self,
    ) -> InfrastructureSurroundingsWrapper:
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=self.infrastructure_section_fom.infrastructuur,
            upkeeping_costs=self.infrastructure_section_fom.opslagfactor_wegen,
            non_rising_dike_costs=self.infrastructure_section_fom.infrakosten_0dh,
        )
        _infra_wrapper.roads_class_2_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_2_polderside")
        )
        _infra_wrapper.roads_class_7_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_7_polderside")
        )
        _infra_wrapper.roads_class_24_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_24_polderside")
        )
        _infra_wrapper.roads_class_47_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_47_polderside")
        )
        _infra_wrapper.roads_class_unknown_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_unknown_polderside")
        )

        return _infra_wrapper


@dataclass
class KoswatSurroundingsWrapperCollectionBuilder(BuilderProtocol):
    surroundings_section_fom: SurroundingsSectionFom
    infrastructure_section_fom: InfrastructureSectionFom

    traject_loc_shp_file: Path
    selected_locations: list[str]

    def _get_dike_locations_shp_fom(self) -> list[KoswatDikeLocationsShpFom]:
        _reader = KoswatDikeLocationsListShpReader()
        _reader.selected_locations = self.selected_locations
        return _reader.read(self.traject_loc_shp_file)

    def build(self) -> list[SurroundingsWrapper]:
        _dike_location_shp = self._get_dike_locations_shp_fom()

        # SHP files currently contain their trajects with a dash '-', whilst the CSV directories have their names with underscore '_'.
        _surroundings_wrappers = []
        for _shp_traject, _location_list in groupby(
            _dike_location_shp, lambda x: x.dike_traject
        ):
            _csv_traject = _shp_traject.replace("-", "_").strip()
            _csv_dir = self.surroundings_section_fom.surroundings_database_dir.joinpath(
                _csv_traject
            )
            if not _csv_dir.is_dir():
                logging.warning(
                    "No surroundings files found for traject %s", _shp_traject
                )
                continue

            _surroundings_wrapper_builder = SurroundingsWrapperBuilder(
                surroundings_section_fom=self.surroundings_section_fom,
                infrastructure_section_fom=self.infrastructure_section_fom,
                surroundings_csv_fom_collection=self._csv_dir_to_fom(_csv_dir),
                location_shp_fom=None,
            )
            for _location in _location_list:
                try:
                    _surroundings_wrapper_builder.location_shp_fom = _location
                    _surroundings_wrappers.append(_surroundings_wrapper_builder.build())
                except Exception as e_info:
                    logging.error(
                        "Could not load surroundings for dike section %s. Detailed error: %s",
                        _location.dike_section,
                        e_info,
                    )

        return _surroundings_wrappers

    def _map_surrounding_type(self, surrounding_type: str) -> str:
        _normalized = surrounding_type.lower().strip()
        _translations = dict(
            bebouwing_binnendijks="buildings_polderside",
            bebouwing_buitendijks="buildings_dikeside",
            spoor_binnendijks="railways_polderside",
            spoor_buitendijks="railways_dikeside",
            water_binnendijks="waters_polderside",
            water_buitendijks="waters_dikeside",
            wegen_binnendijks_klasse2="roads_class_2_polderside",
            wegen_binnendijks_klasse7="roads_class_7_polderside",
            wegen_binnendijks_klasse24="roads_class_24_polderside",
            wegen_binnendijks_klasse47="roads_class_47_polderside",
            wegen_binnendijks_klasseonbekend="roads_class_unknown_polderside",
            wegen_buitendijks_klasse2="roads_class_2_dikeside",
            wegen_buitendijks_klasse7="roads_class_7_dikeside",
            wegen_buitendijks_klasse24="roads_class_24_dikeside",
            wegen_buitendijks_klasse47="roads_class_47_dikeside",
            wegen_buitendijks_klasseonbekend="roads_class_unknown_dikeside",
        )
        _translation = _translations.get(_normalized, None)
        if not _translation:
            _error = "No mapping found for {}".format(surrounding_type)
            logging.error(_error)
            raise ValueError(_error)
        return _translation

    def _csv_file_to_fom(
        self, csv_file: Path, traject_name: str
    ) -> tuple[str, KoswatSurroundingsCsvFom]:
        _surrounding_csv_fom = KoswatSurroundingsCsvReader().read(csv_file)
        _surrounding_csv_fom.traject = traject_name
        _surrounding_type = self._map_surrounding_type(
            csv_file.stem.replace(f"T_{traject_name}_", "")
        )
        return _surrounding_type, _surrounding_csv_fom

    def _csv_dir_to_fom(
        self,
        csv_dir: Path,
    ) -> dict[str, KoswatSurroundingsCsvFom]:
        _imported_csv_foms = {}
        for _csv_file in csv_dir.glob("*.csv"):
            _type, _csv_fom = self._csv_file_to_fom(_csv_file, csv_dir.stem)
            _imported_csv_foms[_type] = _csv_fom
        return _imported_csv_foms
