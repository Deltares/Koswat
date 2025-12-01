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
from pathlib import Path
from typing import List, Tuple

import shapefile
from shapely.geometry import Point

from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


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

        def is_selected(idx_record: Tuple[int, shapefile._Record]) -> bool:
            _, _record = idx_record
            try:
                # TODO: Normalize expected input file to avoid this here and in `KoswatDikeLocationsShpFom`
                return _record.Dijksectie in self.selected_locations
            except Exception:
                return _record.Sectie

        _shp_locations = []
        with shapefile.Reader(file_path) as shp:
            # Records contains Dikesection - Traject - Subtraject
            # For each record get its shape
            # shp.records()[idx] -> shp.shapes()[idx]
            """
            Usual formats are as:
            Dijksectie: `10-1-3-C-1-D-1`.
            Traject: `10-1`
            Subtraject: `10-1-A`
            """
            _shp_locations = list(
                map(
                    record_to_shp_fom,
                    filter(
                        is_selected,
                        enumerate(shp.records()),
                    ),
                )
            )
        return _shp_locations
