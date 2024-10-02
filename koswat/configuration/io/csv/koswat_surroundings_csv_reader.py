import math
import re
from math import isclose
from pathlib import Path

from shapely import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatSurroundingsCsvReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> KoswatSurroundingsCsvFom:
        _csv_fom = KoswatCsvReader().read(file_path)

        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatSurroundingsCsvFom()
        _koswat_fom.distances_list = self._get_surroundings_distances(
            _csv_fom.headers[3:]
        )
        _koswat_fom.points_surroundings_list = self._build_points_surroundings_list(
            _koswat_fom.distances_list, _csv_fom.entries
        )
        return _koswat_fom

    def _get_surroundings_distances(self, distance_list: list[str]) -> list[float]:
        def to_distance_float(header_value: str) -> float:
            _d_values = re.findall(r"\d+", header_value)
            if len(_d_values) != 1:
                raise ValueError(
                    "More than one distance captured, distance headers should be like `afst_42m`."
                )
            return float(_d_values[0])

        return list(map(to_distance_float, distance_list))

    def _build_points_surroundings_list(
        self, distances_list: list[float], entries: list[list[str]]
    ) -> list[PointSurroundings]:
        _point_list = []
        for idx, _point_entry in enumerate(entries):
            _point_entry.insert(0, idx)
            _ps = self._build_point_surroundings(_point_entry, distances_list)
            _point_list.append(_ps)
        return _point_list

    def _build_point_surroundings(
        self, entry: list[str], distances_list: list[float]
    ) -> PointSurroundings:
        def csv_column_to_dict(csv_columns: list[str]) -> dict:
            """
            (Koswat #172) To avoid adding more entries than required,
             - only add keys whose weight is greater than zero,
             - and the keys before them that are zero.
            The keys with zeros act as a limit to avoid adding unnecessary costs
            """
            _tuples_for_dict = []

            def last_tuple_had_weight() -> bool:
                return any(_tuples_for_dict) and not math.isclose(
                    _tuples_for_dict[0][1], 0
                )

            def can_add_item(weight: float) -> bool:
                return weight > 0 or (
                    math.isclose(weight, 0) and last_tuple_had_weight()
                )

            for e_idx, e_val in reversed(list(enumerate(csv_columns))):
                _as_float = float(e_val)
                if can_add_item(_as_float):
                    _tuples_for_dict.insert(0, (distances_list[e_idx], _as_float))

            return dict(_tuples_for_dict)

        return PointSurroundings(
            section=entry[1],
            traject_order=entry[0],
            location=Point(float(entry[2]), float(entry[3])),
            surroundings_matrix=csv_column_to_dict(entry[4:]),
        )
