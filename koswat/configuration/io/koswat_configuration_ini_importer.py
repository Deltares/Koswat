from pathlib import Path
from typing import Iterator, List

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini.koswat_costs_ini_fom import KoswatCostsIniFom
from koswat.configuration.io.ini.koswat_dike_selection_ini_fom import (
    KoswatDikeSelectionIniFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_scenario_ini_fom import KoswatScenarioIniFom
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.io.ini.koswat_ini_reader import KoswatIniReader


class KoswatConfigurationIniImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def get_general_ini(self, reader: KoswatIniReader) -> KoswatGeneralIniFom:
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(self.ini_configuration)

    def get_scenarios(
        self, reader: KoswatIniReader, scenario_dir: Path
    ) -> Iterator[KoswatScenarioIniFom]:
        reader.koswat_ini_fom_type = KoswatScenarioIniFom
        for _ini_file in scenario_dir.glob("*.ini"):
            _scenario: KoswatScenarioIniFom = reader.read(_ini_file)
            _scenario.scenario_name = _ini_file.stem
            yield _scenario
    
    def get_dike_selection(self, reader: KoswatIniReader, ini_file: Path) -> KoswatDikeSelectionIniFom:
        reader.koswat_ini_fom_type = KoswatDikeSelectionIniFom
        return reader.read(ini_file)

    def get_dike_costs(self, reader: KoswatIniReader, ini_file: Path) -> KoswatCostsIniFom:
        reader.koswat_ini_fom_type = KoswatDikeSelectionIniFom
        return reader.read(ini_file)

    def build(self) -> KoswatConfiguration:
        _config = KoswatConfiguration()
        _ini_reader = KoswatIniReader()

        # Get FOMs
        _config.general_ini = self.get_general_ini(_ini_reader)
        _config.dike_selection = self.get_dike_selection(_ini_reader, _config.general_ini.analyse_section.dijksecties_selectie)
        _config.scenarios = list(
            self.get_scenarios(
                _ini_reader, _config.general_ini.analyse_section.scenario_invoer
            )
        )
        _config.costs = self.get_dike_costs(_ini_reader, _config.general_ini.analyse_section.eenheidsprijzen)

        return _config
