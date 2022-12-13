import logging
from pathlib import Path
from typing import Iterator, List

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini import (
    KoswatCostsIniFom,
    KoswatGeneralIniFom,
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.configuration.models import KoswatCosts, KoswatDikeSelection, KoswatScenario
from koswat.configuration.models.koswat_general_settings import (
    AnalysisSettings,
    SurroundingsSettings,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


class KoswatConfigurationImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def get_general_ini(self) -> KoswatGeneralIniFom:
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(self.ini_configuration)

    def get_scenarios(
        self, reader: KoswatIniReader, scenario_dir: Path
    ) -> Iterator[KoswatScenario]:
        reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
        for _ini_file in scenario_dir.glob("*.ini"):
            _section_scenarios: KoswatSectionScenariosIniFom = reader.read(_ini_file)
            _section_scenarios.section_name = _ini_file.stem
            for _s_scenario in _section_scenarios.section_scenarios:
                yield _s_scenario

    def get_dike_selection(self, txt_file: Path) -> KoswatDikeSelection:
        _reader = KoswatTxtReader()
        _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
        return _reader.read(txt_file)

    def get_dike_costs(self, reader: KoswatIniReader, ini_file: Path) -> KoswatCosts:
        reader.koswat_ini_fom_type = KoswatCostsIniFom
        return reader.read(ini_file)

    def get_dike_input_profiles(self, csv_file: Path) -> List[KoswatInputProfileBase]:
        pass

    def _get_analysis_settings(self, ini_fom: KoswatGeneralIniFom) -> AnalysisSettings:
        _ini_reader = KoswatIniReader()
        _settings = AnalysisSettings()
        _settings.dike_selection = self.get_dike_selection(
            ini_fom.analyse_section.dike_sections_selection_ini_file
        )
        _settings.scenarios = list(
            self.get_scenarios(_ini_reader, ini_fom.analyse_section.scenarios_dir)
        )
        _settings.costs = self.get_dike_costs(
            _ini_reader, ini_fom.analyse_section.costs_ini_file
        )
        _settings.analysis_output = ini_fom.analyse_section.analysis_output_dir
        _settings.dijksectie_ligging = ini_fom.analyse_section.dijksectie_ligging
        _settings.dike_section_input_profiles = (
            ini_fom.analyse_section.dijksectie_invoer
        )
        _settings.include_taxes = ini_fom.analyse_section.include_taxes
        return _settings

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
        _config.analysis_settings = self._get_analysis_settings(_ini_settings)
        _config.dike_profile_settings = _ini_settings.dijkprofiel_section
        _config.soil_settings = _ini_settings.dijkprofiel_section
        _config.pipingwall_settings = _ini_settings.dijkprofiel_section
        _config.stabilitywall_settings = _ini_settings.dijkprofiel_section
        _config.cofferdam_settings = _ini_settings.dijkprofiel_section
        _config.surroundings_settings = _ini_settings.dijkprofiel_section
        _config.infrastructure_settings = _ini_settings.dijkprofiel_section

        logging.info("Importing INI configuration completed.")
        return _config
