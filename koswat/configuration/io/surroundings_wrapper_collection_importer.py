"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from copy import deepcopy
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from koswat.configuration.io.config_sections import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.csv.koswat_simple_surroundings_csv_reader import (
    KoswatSimpleSurroundingsCsvReader,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_reader import (
    KoswatSurroundingsCsvReader,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsListShpReader,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.infrastructure_types import (
    InfrastructureTypeBuilder,
    InfrastructureTypeProtocol,
)
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

    surroundings_database_dir: Path
    surroundings_section_fom: SurroundingsSectionFom
    infrastructure_section_fom: InfrastructureSectionFom

    traject_loc_shp_file: Path
    selected_locations: list[str]
    infrastructure_costs: InfrastructureCostsSettings

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
            # Map SHP traject name to CSV directory name.
            _csv_traject = _shp_traject.replace("-", "_").strip()
            _csv_dir = self.surroundings_database_dir.joinpath(_csv_traject)
            if not _csv_dir.is_dir():
                logging.warning(
                    "No surroundings files found for traject %s", _shp_traject
                )
                continue

            # Build surroundings wrappers for all locations in the traject.
            _obstacles, _infrastructures = self._csv_dir_to_fom(
                _csv_dir, self.surroundings_section_fom.obstacle_types
            )
            _surroundings_wrapper_builder = SurroundingsWrapperBuilder(
                surroundings_section_fom=self.surroundings_section_fom,
                infrastructure_section_fom=self.infrastructure_section_fom,
                obstacles=_obstacles,
                infrastructures=_infrastructures,
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

    def _csv_obstacle_file_to_fom(
        self,
        csv_file: Path,
        surrounding_buffer: float,
    ) -> KoswatSurroundingsCsvFom:
        _reader = KoswatSimpleSurroundingsCsvReader()
        _reader.surroundings_buffer = surrounding_buffer
        return _reader.read(csv_file)

    def _process_obstacle_file(
        self,
        obstacle_type: str,
        csv_file: Path,
        obstacle_csv_fom: KoswatSurroundingsCsvFom,
    ) -> KoswatSurroundingsCsvFom:
        _buffer = self.surroundings_section_fom.obstacle_types.get(obstacle_type, 0.0)
        _csv_fom = self._csv_obstacle_file_to_fom(csv_file, _buffer)
        if obstacle_csv_fom is not None:
            obstacle_csv_fom.merge(_csv_fom)
            return obstacle_csv_fom

        return _csv_fom

    def _csv_infrastructure_file_to_fom(
        self,
        csv_file: Path,
    ) -> KoswatSurroundingsCsvFom:
        return KoswatSurroundingsCsvReader().read(csv_file)

    def _process_infrastructure_file(
        self,
        infrastructure_type: InfrastructureTypeProtocol,
        csv_file: Path,
        infrastructure_csv_foms: dict[
            InfrastructureTypeProtocol, KoswatSurroundingsCsvFom
        ],
    ) -> KoswatSurroundingsCsvFom:
        _csv_fom = self._csv_infrastructure_file_to_fom(csv_file)
        _existing_fom = next(
            (
                _fom
                for _rc, _fom in infrastructure_csv_foms.items()
                if _rc.infrastructure_name == infrastructure_type.infrastructure_name
            ),
            None,
        )
        if _existing_fom:
            if not infrastructure_type.is_polderside:
                _existing_fom.merge(_csv_fom)
                return _existing_fom
            _csv_fom.merge(_existing_fom)

        return _csv_fom

    def _csv_dir_to_fom(self, csv_dir: Path, obstacle_types: dict[str, float]) -> tuple[
        KoswatSurroundingsCsvFom,
        dict[InfrastructureTypeProtocol, KoswatSurroundingsCsvFom],
    ]:
        """
        Converts all CSV surrounding files in the provided `csv_dir` into a dictionary of
        `KoswatSurroundingsCsvFom` objects, grouped by their type name.

        Args:
            csv_dir (Path): The directory containing the CSV files.
            obstacle_types (dict[str, float]): A dictionary of custom obstacle names and their corresponding buffer values.

        Returns:
            tuple[
                KoswatSurroundingsCsvFom, dict[RoadClassProtocol, KoswatSurroundingsCsvFom]
            ]: A tuple containing the obstacle CSV FOM and a dictionary of infrastructure CSV FOMs, grouped by their type name.
        """
        _obstacle_csv_fom: KoswatSurroundingsCsvFom = None
        _infrastructure_csv_foms: dict[
            InfrastructureTypeProtocol, KoswatSurroundingsCsvFom
        ] = {}

        _traject_name = csv_dir.stem
        _read_obs_types = []
        _first_fom: KoswatSurroundingsCsvFom | None = None
        _infrastructure_type_builder = InfrastructureTypeBuilder(
            infrastructure_section=self.infrastructure_section_fom,
            infrastructure_costs=self.infrastructure_costs,
        )
        for _csv_file in csv_dir.glob("*.csv"):
            _type_name = _csv_file.stem.replace(f"T_{_traject_name}_", "")
            # Try to map file name an infrastructure surrounding type.
            _infrastructure_type = _infrastructure_type_builder.build(_type_name)

            if not _infrastructure_type:
                # Obstacle surrounding type
                if _type_name not in obstacle_types:
                    # In case of obstacles, only import those that are defined in the config file.
                    logging.info(
                        f"Skipping obstacle surrounding type {_type_name} for traject {_traject_name} as it is not defined in the config file."
                    )
                    continue

                _csv_fom = self._process_obstacle_file(
                    _type_name, _csv_file, _obstacle_csv_fom
                )
                _obstacle_csv_fom = _csv_fom
                _read_obs_types.append(_type_name)
            else:
                _csv_fom = self._process_infrastructure_file(
                    _infrastructure_type, _csv_file, _infrastructure_csv_foms
                )
                _infrastructure_csv_foms[_infrastructure_type] = _csv_fom

            if _first_fom is None:
                _first_fom = deepcopy(_csv_fom)
            else:
                if not _first_fom.locations_identical(_csv_fom):
                    raise ValueError(
                        "Location mismatch detected between the first imported surroundings and the current."
                    )

        # Log missing obstacle files.
        for _obs_type in obstacle_types:
            if _obs_type not in _read_obs_types:
                logging.warning(
                    f"Obstacle surrounding type {_obs_type} defined in config file is missing for traject {_traject_name}."
                )

        return _obstacle_csv_fom, _infrastructure_csv_foms
