import logging
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from koswat.configuration.io.csv.koswat_simple_surroundings_csv_reader import KoswatSimpleSurroundingsCsvReader
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
from koswat.dike.surroundings.surroundings_enum import SurroundingsEnum
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


@dataclass
class SurroundingsWrapperCollectionImporter(BuilderProtocol):
    """
    This importer actually behaves as a "builder" as it does not directly
    import from one source but a combination of many. To avoid bypassing
    the protocol's signatures it inherits from the `BuilderProtocol` instead.
    """

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

        print( f"Imported {len(_surroundings_wrappers)} surroundings wrappers." )
        return _surroundings_wrappers

    def _csv_file_to_fom(
        self, csv_file: Path, traject_name: str
    ) -> tuple[SurroundingsEnum, KoswatSurroundingsCsvFom]:
        _surrounding_type = SurroundingsEnum.translate(
            csv_file.stem.replace(f"T_{traject_name}_", "")
        )
        _reader = KoswatSurroundingsCsvReader
        if _surrounding_type.surrounding_type == SurroundingsObstacle:
            _reader = KoswatSimpleSurroundingsCsvReader
            
        _surrounding_csv_fom = _reader().read(csv_file)
        _surrounding_csv_fom.traject = traject_name
        return _surrounding_type, _surrounding_csv_fom

    def _csv_dir_to_fom(
        self,
        csv_dir: Path,
    ) -> dict[str, KoswatSurroundingsCsvFom]:
        _imported_csv_foms = {}
        for _csv_file in csv_dir.glob("*.csv"):
            _type, _csv_fom = self._csv_file_to_fom(_csv_file, csv_dir.stem)
            _imported_csv_foms[_type.name] = _csv_fom
        return _imported_csv_foms
