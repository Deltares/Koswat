
from pathlib import Path

import shapefile
from shapely.geometry import Point

from koswat.io.koswat_reader_protocol import (
    FileObjectModelProtocol,
    KoswatReaderProtocol,
)


class KoswatShpModel(FileObjectModelProtocol):
    initial_point: Point
    end_point: Point

class KoswatShpReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> KoswatShpModel:
        if not isinstance(file_path, Path) or file_path.suffix != ".shp": 
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        
        _shp_model = KoswatShpModel()
        with shapefile.Reader(file_path) as shp:
            _shp_points = shp.shapes()[0].points
            _shp_model.initial_point = Point(_shp_points[0])
            _shp_model.end_point = Point(_shp_points[-1])
        return _shp_model
        