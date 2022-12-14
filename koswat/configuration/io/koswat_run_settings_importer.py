import logging
from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.converters.koswat_settings_fom_to_run_settings import (
    KoswatSettingsFomToRunSettings,
)
from koswat.configuration.io.ini import KoswatSettingsIniFom
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatRunSettingsImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def build(self) -> KoswatRunSettings:
        # First get the FOM
        logging.info(
            "Importing INI configuration from {}".format(self.ini_configuration)
        )
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatSettingsIniFom
        _fom_settings = reader.read(self.ini_configuration)
        logging.info("Importing INI configuration completed.")

        # Then convert to DOM
        logging.info("Mapping data to Koswat Settings")
        _run_settings = KoswatSettingsFomToRunSettings.with_settings_fom(_fom_settings).build()
        logging.info("Settings import completed.")

        return _run_settings
