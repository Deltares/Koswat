from typing import Dict, List

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniFom(FileObjectModelProtocol):
    section = Dict[str, str]
    ini_file = Dict[str, section]
    #    sections = Dict[str, List(section, str)]
    #    points_surroundings_list: List[PointSurroundings]
    #    distances_list: List[float]

    def __init__(self) -> None:
        self.section = []
        self.ini_file = []

    #        self.points_surroundings_list = []
    #        self.distances_list = []

    def is_valid(self) -> bool:
        return True


#       return self.points_surroundings_list and any(self.points_surroundings_list)
