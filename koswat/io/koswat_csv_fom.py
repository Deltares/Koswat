import re
from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol
from koswat.surroundings.koswat_buildings_polderside import PointSurroundings


class KoswatCsvFom(FileObjectModelProtocol):
    points_surroundings_list: List[PointSurroundings] = []
    distances_list: List[float] = []

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)


class KoswatCsvFomBuilder(BuilderProtocol):
    headers: List[str] = []
    entries: List[List[str]] = []

    def _is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)
        return all(map(lambda x: len(x) == _l_header, self.entries))

    def _get_surroundings_distances(self, distance_list: List[str]) -> List[float]:
        def to_distance_float(header_value: str) -> float:
            _d_values = re.findall(r"\d+", header_value)
            if len(_d_values) != 1:
                raise ValueError(
                    "More than one distance captured, distance headers should be like `afst_42m`."
                )
            return float(_d_values[0])

        return list(map(to_distance_float, distance_list))

    def _build_point_surroundings(
        self, entry: List[str], distances_list: List[float]
    ) -> PointSurroundings:
        _point = PointSurroundings()
        _point.section = entry[0]
        _x_coord = float(entry[1])
        _y_coord = float(entry[2])
        _point.location = Point((_x_coord, _y_coord))
        _point.distance_to_buildings = [
            distances_list[e_idx]
            for e_idx, e_val in enumerate(entry[3:])
            if e_val == "1"
        ]
        return _point

    def _build_points_surroundings_list(
        self, distances_list: List[float]
    ) -> List[PointSurroundings]:
        return list(
            map(
                lambda x: self._build_point_surroundings(x, distances_list),
                self.entries,
            )
        )

    def build(self) -> KoswatCsvFom:
        if not self._is_valid():
            raise ValueError("Not valid headers and entries combination.")
        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatCsvFom()
        _koswat_fom.distances_list = self._get_surroundings_distances(self.headers[3:])
        _koswat_fom.points_surroundings_list = self._build_points_surroundings_list(
            _koswat_fom.distances_list
        )
        return _koswat_fom
