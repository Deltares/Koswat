from typing import List

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class KoswatSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: List[PointSurroundings]
    distances_list: List[float]
    traject: str

    def __init__(self) -> None:
        self.points_surroundings_list = []
        self.distances_list = []
        self.traject = ""

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)
