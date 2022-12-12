from typing import List

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.koswat_reader_protocol import ImportFileObjectModelProtocol


class KoswatCsvFom(ImportFileObjectModelProtocol):
    points_surroundings_list: List[PointSurroundings]
    distances_list: List[float]

    def __init__(self) -> None:
        self.points_surroundings_list = []
        self.distances_list = []

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)
