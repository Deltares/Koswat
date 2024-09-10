import re
from pathlib import Path

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_builder import (
    PointSurroundingsBuilder,
)


class KoswatSurroundingsCsvReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> KoswatTrajectSurroundingsCsvFom:
        _csv_fom = KoswatCsvReader().read(file_path)

        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatTrajectSurroundingsCsvFom()
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

    def _build_point_surroundings(
        self, entry: list[str], distances_list: list[float]
    ) -> PointSurroundings:
        _point_dict = dict(
            traject_order=entry[0],
            section=entry[1],
            location=(float(entry[2]), float(entry[3])),
            surroundings_matrix={
                distances_list[e_idx]: float(e_val)
                for e_idx, e_val in enumerate(entry[4:])
            },
        )
        _builder = PointSurroundingsBuilder()
        _builder.point_surroundings_data = _point_dict
        return _builder.build()

    def _build_points_surroundings_list(
        self, distances_list: list[float], entries: list[list[str]]
    ) -> list[PointSurroundings]:
        _point_list = []
        for idx, _point_entry in enumerate(entries):
            _point_entry.insert(0, idx)
            _ps = self._build_point_surroundings(_point_entry, distances_list)
            _point_list.append(_ps)
        return _point_list
