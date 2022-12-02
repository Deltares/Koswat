from typing import Dict, List

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class KoswatIniFom(FileObjectModelProtocol):
    section = Dict[str, str]
    ini_file = Dict[str, section]

    def __init__(self) -> None:
        #        self.section = [] # TODO needed?
        self.ini_file = []

    def is_valid(self) -> bool:
        # TODO add validation
        return True
