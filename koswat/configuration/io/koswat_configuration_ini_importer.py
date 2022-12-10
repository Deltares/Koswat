from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini.koswat_general_ini_fom import KoswatGeneralIniFom
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatConfigurationIniImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def get_general_ini(self, reader: KoswatIniReader) -> KoswatGeneralIniFom:
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(self.ini_configuration)

    def build(self) -> KoswatConfiguration:
        _configuration = KoswatConfiguration()
        _ini_reader = KoswatIniReader()

        # Get FOMs
        _general_ini = self.get_general_ini(_ini_reader)

        return _configuration
