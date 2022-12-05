from typing import Dict

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
