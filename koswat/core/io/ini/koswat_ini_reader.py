import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


@dataclass
class KoswatIniReader(KoswatReaderProtocol):

    koswat_ini_fom_type: Type[KoswatIniFomProtocol] = None

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
        return self.koswat_ini_fom_type.from_config(_ini_parser)
