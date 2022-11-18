from pathlib import Path

import shapefile
from shapely.geometry import Point

from koswat.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.io.shp import KoswatShpFom


class KoswatShpReader(KoswatReaderProtocol):
    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".shp"

    def read(self, file_path: Path) -> KoswatShpFom:
        if not self.supports_file(file_path):
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _shp_model = KoswatShpFom()
        with shapefile.Reader(file_path) as shp:
            _shp_points = shp.shapes()[0].points
            _shp_model.initial_point = Point(_shp_points[0])
            _shp_model.end_point = Point(_shp_points[-1])
        return _shp_model