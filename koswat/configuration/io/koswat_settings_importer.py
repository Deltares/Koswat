import logging
from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini import KoswatSettingsIniFom
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatSettingsFomImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def build(self) -> KoswatSettingsIniFom:
        logging.info(
            "Importing INI configuration from {}".format(self.ini_configuration)
        )

        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatSettingsIniFom
        _fom_settings = reader.read(self.ini_configuration)
        logging.info("Importing INI configuration completed.")

        return _fom_settings
