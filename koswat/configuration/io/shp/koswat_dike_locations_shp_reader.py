from pathlib import Path

import shapefile
from shapely.geometry import Point

from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatDikeLocationsShpReader(KoswatReaderProtocol):
    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix.lower() == ".shp"

    def read(self, file_path: Path) -> KoswatDikeLocationsShpFom:
        if not self.supports_file(file_path):
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _shp_model = KoswatDikeLocationsShpFom()
        with shapefile.Reader(file_path) as shp:
            # Records contains Dikesection - Traject - Subtraject            
            _shp_model.records = shp.records()
            # For each record get its shape
            # shp.records()[0] -> shp.shapes()[0]
            # Only getting the first shape
            _shp_points = shp.shapes()[0].points
            _shp_model.initial_point = Point(_shp_points[0])
            _shp_model.end_point = Point(_shp_points[-1])
        return _shp_model
