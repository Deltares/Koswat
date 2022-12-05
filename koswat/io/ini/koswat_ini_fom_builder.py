import configparser
from typing import Dict

from koswat.builder_protocol import BuilderProtocol
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

        # TODO read and process ini file, get dict from configparser
        config = configparser.ConfigParser()
        config.read(path)
        config.get

        ini_file = Dict[str, Dict[str, str]]
        return ini_file

    def build(self, path) -> KoswatIniFom:
        if not self._is_valid():
            raise ValueError("Not valid ini file.")

        _koswat_fom = KoswatIniFom()
        _koswat_fom.ini_file = self.get_ini_file(path)

        return _koswat_fom
