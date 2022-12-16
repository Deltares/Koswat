import logging
from pathlib import Path
from typing import Any, Iterator, List

import shapefile
from shapely.geometry import Point

from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
    KoswatDikeLocationsWrapperShpFom,
)
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatDikeLocationsWrapperShpReader(KoswatReaderProtocol):
    selected_locations: List[str]

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix.lower() == ".shp"

    def _get_selected_records_idx(self, shp_records) -> List[int]:
        if not self.selected_locations:
            return list(range(0, len(shp_records)))
        _idx_list = []
        for idx, _record in enumerate(shp_records):
            if _record.Dijksectie in self.selected_locations:
                _idx_list.append(idx)
        return _idx_list

    def read(self, file_path: Path) -> KoswatDikeLocationsWrapperShpFom:
        if not self.supports_file(file_path):
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        if not self.selected_locations:
            logging.warning("No selected locations.")

        _shp_wrapper = KoswatDikeLocationsWrapperShpFom()
        with shapefile.Reader(file_path) as shp:
            # Records contains Dikesection - Traject - Subtraject
            # For each record get its shape
            # shp.records()[0] -> shp.shapes()[0]
            # Only getting the first shape
            for _idx in self._get_selected_records_idx(shp.records()):
                _shp_fom = KoswatDikeLocationsShpFom()
                _shp_points = shp.shape(_idx).points
                _shp_fom.initial_point = Point(_shp_points[0])
                _shp_fom.end_point = Point(_shp_points[-1])
                _shp_fom.record = shp.record(_idx)
                _shp_wrapper.dike_locations_shp_fom.append(_shp_fom)
        return _shp_wrapper
