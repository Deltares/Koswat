import logging
from itertools import groupby
from pathlib import Path

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_reader import (
    KoswatSurroundingsCsvReader,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsListShpReader,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


class KoswatSurroundingsImporter(KoswatImporterProtocol):
    traject_loc_shp_file: Path
    selected_locations: list[str]

    def __init__(self) -> None:
        self.traject_loc_shp_file = None
        self.selected_locations = []

    def _get_dike_locations_shp_fom(self) -> list[KoswatDikeLocationsShpFom]:
        _reader = KoswatDikeLocationsListShpReader()
        _reader.selected_locations = self.selected_locations
        return _reader.read(self.traject_loc_shp_file)

    def import_from(
        self, surroundings_section: SurroundingsSectionFom
    ) -> list[SurroundingsWrapper]:
        _from_path = surroundings_section.surroundings_database_dir
        if not isinstance(_from_path, Path):
            raise ValueError("No surroundings csv directory path given.")
        if not isinstance(self.traject_loc_shp_file, Path):
            raise ValueError("No traject shp file path given.")

        _dike_location_shp = self._get_dike_locations_shp_fom()

        # SHP files currently contain their trajects with a dash '-', whilst the CSV directories have their names with underscore '_'.
        _surroundings_wrappers = []
        for _shp_traject, _location_list in groupby(
            _dike_location_shp, lambda x: x.dike_traject
        ):
            _csv_traject = _shp_traject.replace("-", "_").strip()
            _csv_dir = _from_path.joinpath(_csv_traject)
            if not _csv_dir.is_dir():
                logging.warning(
                    "No surroundings files found for traject {}".format(_shp_traject)
                )
                continue

            _surroudings_fom = self._csv_dir_to_fom(_csv_dir)
            for _location in _location_list:
                try:
                    _surroundings_wrappers.append(
                        SurroundingsWrapperBuilder(
                            trajects_fom=_location,
                            surroundings_fom=_surroudings_fom,
                            surroundings_section=surroundings_section,
                        ).build()
                    )
                except Exception as e_info:
                    logging.error(
                        "Could not load surroundings for dike section {}. Detailed error: {}".format(
                            _location.dike_section, e_info
                        )
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
    ) -> tuple[str, KoswatTrajectSurroundingsCsvFom]:
        _surrounding_csv_fom = KoswatSurroundingsCsvReader().read(csv_file)
        _surrounding_csv_fom.traject = traject_name
        _surrounding_type = self._map_surrounding_type(
            csv_file.stem.replace(f"T_{traject_name}_", "")
        )
        return _surrounding_type, _surrounding_csv_fom

    def _csv_dir_to_fom(
        self,
        csv_dir: Path,
    ) -> KoswatTrajectSurroundingsWrapperCsvFom:
        _surroundings_wrapper = KoswatTrajectSurroundingsWrapperCsvFom()
        _surroundings_wrapper.traject = csv_dir.stem
        for _csv_file in csv_dir.glob("*.csv"):
            _type, _csv_fom = self._csv_file_to_fom(_csv_file, csv_dir.stem)
            setattr(_surroundings_wrapper, _type, _csv_fom)
        return _surroundings_wrapper
