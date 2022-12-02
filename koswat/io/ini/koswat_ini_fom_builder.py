import configparser
import re
from typing import Dict, List

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_builder import (
    PointSurroundingsBuilder,
)
from koswat.io.ini.koswat_ini_fom import KoswatIniFom


class KoswatIniFomBuilder(BuilderProtocol):
    #    headers: List[str]
    #    entries: List[List[str]]

    def __init__(self) -> None:
        #        self.headers = []
        #        self.entries = []
        self.sections = []

    def _is_valid(self) -> bool:
        # if not self.headers or not self.entries:
        #     return False
        # _l_header = len(self.headers)
        # return all(map(lambda x: len(x) == _l_header, self.entries))
        return False

    def get_ini_file(self, path) -> Dict[str, Dict[str, str]]:
        # if not self.headers or not self.entries:
        #     return False
        # _l_header = len(self.headers)
        # return all(map(lambda x: len(x) == _l_header, self.entries))

        # TODO read and process ini file
        config = configparser.ConfigParser()
        config.read(path)
        config.get

        ini_file = Dict[str, Dict[str, str]]
        return ini_file

    # def _get_surroundings_distances(self, distance_list: List[str]) -> List[float]:
    #     def to_distance_float(header_value: str) -> float:
    #         _d_values = re.findall(r"\d+", header_value)
    #         if len(_d_values) != 1:
    #             raise ValueError(
    #                 "More than one distance captured, distance headers should be like `afst_42m`."
    #             )
    #         return float(_d_values[0])

    #     return list(map(to_distance_float, distance_list))

    # def _build_point_surroundings(
    #     self, entry: List[str], distances_list: List[float]
    # ) -> PointSurroundings:
    #     _point_dict = dict(
    #         traject_order=entry[0],
    #         section=entry[1],
    #         location=(float(entry[2]), float(entry[3])),
    #         distance_to_buildings=[
    #             distances_list[e_idx]
    #             for e_idx, e_val in enumerate(entry[4:])
    #             if e_val == "1"
    #         ],
    #     )
    #     _builder = PointSurroundingsBuilder()
    #     _builder.point_surroundings_data = _point_dict
    #     return _builder.build()

    # def _build_points_surroundings_list(
    #     self, distances_list: List[float]
    # ) -> List[PointSurroundings]:
    #     _point_list = []
    #     for idx, _point_entry in enumerate(self.entries):
    #         _point_entry.insert(0, idx)
    #         _ps = self._build_point_surroundings(_point_entry, distances_list)
    #         _point_list.append(_ps)
    #     return _point_list

    def build(self, path) -> KoswatIniFom:
        if not self._is_valid():
            raise ValueError("Not valid ini file.")
        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatIniFom()
        _koswat_fom.ini_file = self.get_ini_file(path)
        #        _koswat_fom.distances_list = self._get_surroundings_distances(self.headers[3:])
        #        _koswat_fom.points_surroundings_list = self._build_points_surroundings_list(
        #            _koswat_fom.distances_list
        #        )
        return _koswat_fom
