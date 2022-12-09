import configparser
from pathlib import Path
from typing import Type

from koswat.io.ini.koswat_general_ini_fom import KoswatIniFomProtocol
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatIniReader(KoswatReaderProtocol):

    koswat_ini_fom_type: Type[KoswatIniFomProtocol]

    def __init__(self) -> None:
        self.koswat_ini_fom_type = None

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".ini"

    def read(self, file_path: Path) -> KoswatIniFomProtocol:
        if not self.supports_file(file_path):
            raise ValueError("Ini file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        if not self.koswat_ini_fom_type:
            raise ValueError("KoswatIniFom type needs to be specified.")

        _ini_parser = configparser.ConfigParser(comment_prefixes="#")
        # !IMPORTANT! CONFIGPARSER Sections are case sensitive whilst options are not.
        # https://docs.python.org/3.10/library/configparser.html#mapping-protocol-access
        _ini_parser.read(file_path)
        return self.koswat_ini_fom_type.from_dict(_ini_parser)
