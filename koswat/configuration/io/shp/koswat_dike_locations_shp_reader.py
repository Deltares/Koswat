import logging
from pathlib import Path
from typing import List, Tuple

import shapefile
from shapely.geometry import Point

from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatDikeLocationsListShpReader(KoswatReaderProtocol):
    selected_locations: List[str]

    def __init__(self) -> None:
        self.selected_locations = []

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix.lower() == ".shp"

    def read(self, file_path: Path) -> List[KoswatDikeLocationsShpFom]:
        if not self.supports_file(file_path):
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        if not self.selected_locations:
            logging.warning("No selected locations.")

        def record_to_shp_fom(
            idx_record: Tuple[int, shapefile._Record]
        ) -> KoswatDikeLocationsShpFom:
            _idx, _record = idx_record
            _shp_fom = KoswatDikeLocationsShpFom()
            _shp_points = shp.shape(_idx).points
            _shp_fom.initial_point = Point(_shp_points[0])
            _shp_fom.end_point = Point(_shp_points[-1])
            _shp_fom.record = _record
            return _shp_fom

        def is_selected_record(record: shapefile._Record) -> bool:
            """
            Verifies the record 'Dijksectie' property is a value from the list of selected dikes (provided by the user).
            Usual formats are as:
            Dijksectie: `10-1-3-C-1-D-1`.
            Traject: `10-1`
            Subtraject: `10-1-A

            Returns:
                bool: True when the record has been selected.
            """
            return record.Dijksectie in self.selected_locations

        _shp_locations = []
        with shapefile.Reader(file_path) as shp:
            # Records contains Dikesection - Traject - Subtraject
            # For each record get its shape
            # shp.records()[idx] -> shp.shapes()[idx]
            _shp_locations = list(
                map(
                    record_to_shp_fom,
                    enumerate(filter(is_selected_record, shp.records())),
                )
            )
        return _shp_locations
