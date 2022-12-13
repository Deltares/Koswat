import logging
from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.converters import (
    koswat_analysis_converter as AnalysisConverter,
)
from koswat.configuration.io.ini import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.configuration.models.koswat_general_settings import SurroundingsSettings
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatConfigurationImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def get_general_ini(self) -> KoswatGeneralIniFom:
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(self.ini_configuration)

    def _get_surroundings_settings(
        self, surroundings_fom: SurroundingsSectionFom
    ) -> SurroundingsSettings:
        _settings = SurroundingsSettings()
        _settings.constructieafstand = surroundings_fom.constructieafstand
        _settings.constructieovergang = surroundings_fom.constructieovergang
        _settings.buitendijks = surroundings_fom.buitendijks
        _settings.bebouwing = surroundings_fom.bebouwing
        _settings.spoorwegen = surroundings_fom.spoorwegen
        _settings.water = surroundings_fom.water
        _settings.surroundings_database = surroundings_fom.omgevingsdatabases
        return _settings

    def build(self) -> KoswatConfiguration:
        logging.info(
            "Importing INI configuration from {}".format(self.ini_configuration)
        )

        _config = KoswatConfiguration()

        # Get FOMs
        _ini_settings = self.get_general_ini()
        _config.analysis_settings = AnalysisConverter.analysis_settings_fom_to_dom(
            _ini_settings.analyse_section
        )
        _config.dike_profile_settings = _ini_settings.dijkprofiel_section
        _config.soil_settings = _ini_settings.dijkprofiel_section
        _config.pipingwall_settings = _ini_settings.dijkprofiel_section
        _config.stabilitywall_settings = _ini_settings.dijkprofiel_section
        _config.cofferdam_settings = _ini_settings.dijkprofiel_section
        _config.surroundings_settings = _ini_settings.dijkprofiel_section
        _config.infrastructure_settings = _ini_settings.dijkprofiel_section

        logging.info("Importing INI configuration completed.")
        return _config
