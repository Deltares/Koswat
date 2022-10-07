import re
from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_builder import (
    PointSurroundingsBuilder,
)
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatCsvFom(FileObjectModelProtocol):
    points_surroundings_list: List[PointSurroundings]
    distances_list: List[float]

    def __init__(self) -> None:
        self.points_surroundings_list = []
        self.distances_list = []

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)


class KoswatCsvFomBuilder(BuilderProtocol):
    headers: List[str]
    entries: List[List[str]]

    def __init__(self) -> None:
        self.headers = []
        self.entries = []

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
        _point_dict = dict(
            section=entry[0],
            location=(float(entry[1]), float(entry[2])),
            distance_to_buildings=[
                distances_list[e_idx]
                for e_idx, e_val in enumerate(entry[3:])
                if e_val == "1"
            ],
        )
        _builder = PointSurroundingsBuilder()
        _builder.point_surroundings_data = _point_dict
        return _builder.build()

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
