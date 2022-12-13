import logging
from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.converters import (
    koswat_analysis_converter as AnalysisConverter,
)
from koswat.configuration.io.ini import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.models.koswat_general_settings import (
    KoswatGeneralSettings,
    SurroundingsSettings,
)
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
        _settings.surroundings_database = surroundings_fom.surroundings_database
        return _settings

    def build(self) -> KoswatGeneralSettings:
        logging.info(
            "Importing INI configuration from {}".format(self.ini_configuration)
        )

        _settings = KoswatGeneralSettings()

        # Get FOMs
        _ini_settings = self.get_general_ini()
        _settings.analysis_settings = AnalysisConverter.analysis_settings_fom_to_dom(
            _ini_settings.analyse_section
        )
        _settings.dike_profile_settings = _ini_settings.dijkprofiel_section
        _settings.soil_settings = _ini_settings.grondmaatregel_section
        _settings.pipingwall_settings = _ini_settings.kwelscherm_section
        _settings.stabilitywall_settings = _ini_settings.stabiliteitswand_section
        _settings.cofferdam_settings = _ini_settings.kistdam_section
        _settings.surroundings_settings = _ini_settings.surroundings_section
        _settings.infrastructure_settings = _ini_settings.infrastructuur_section

        logging.info("Importing INI configuration completed.")
        return _settings
