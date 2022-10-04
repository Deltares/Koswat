
from pathlib import Path
from typing import Any

import shapefile

from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatShpModel:
    pass

class KoswatShpReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> Any:
        if not isinstance(file_path, Path) or file_path.suffix != ".shp": 
            raise ValueError("Shp file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        
        _shp_model = KoswatShpModel()
        with shapefile.Reader(file_path) as shp:
            pass
        return None
        