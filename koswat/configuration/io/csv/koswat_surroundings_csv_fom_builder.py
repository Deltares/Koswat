import re
from typing import List

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_builder_protocol import (
    KoswatCsvFomBuilderProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_builder import (
    PointSurroundingsBuilder,
)


class KoswatSurroundingsCsvFomBuilder(KoswatCsvFomBuilderProtocol):
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
            traject_order=entry[0],
            section=entry[1],
            location=(float(entry[2]), float(entry[3])),
            distance_to_buildings=[
                distances_list[e_idx]
                for e_idx, e_val in enumerate(entry[4:])
                if e_val == "1"
            ],
        )
        _builder = PointSurroundingsBuilder()
        _builder.point_surroundings_data = _point_dict
        return _builder.build()

    def _build_points_surroundings_list(
        self, distances_list: List[float]
    ) -> List[PointSurroundings]:
        _point_list = []
        for idx, _point_entry in enumerate(self.entries):
            _point_entry.insert(0, idx)
            _ps = self._build_point_surroundings(_point_entry, distances_list)
            _point_list.append(_ps)
        return _point_list

    def build(self) -> KoswatTrajectSurroundingsCsvFom:
        if not self._is_valid():
            raise ValueError("Not valid headers and entries combination.")
        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatTrajectSurroundingsCsvFom()
        _koswat_fom.distances_list = self._get_surroundings_distances(self.headers[3:])
        _koswat_fom.points_surroundings_list = self._build_points_surroundings_list(
            _koswat_fom.distances_list
        )
        return _koswat_fom

    @classmethod
    def from_text(cls, csv_entries: List[List[str]]) -> KoswatCsvFomBuilderProtocol:
        _builder = cls()
        _builder.headers = csv_entries.pop(0)
        _builder.entries = csv_entries
        return _builder
