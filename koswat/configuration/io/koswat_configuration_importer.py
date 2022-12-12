from pathlib import Path
from typing import Iterator

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini import (
    KoswatCostsIniFom,
    KoswatGeneralIniFom,
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.configuration.models import KoswatCosts, KoswatDikeSelection, KoswatScenario
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


class KoswatConfigurationImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def get_general_ini(self, reader: KoswatIniReader) -> KoswatGeneralIniFom:
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
                yield super(KoswatScenario, _s_scenario)

    def get_dike_selection(self, txt_file: Path) -> KoswatDikeSelection:
        _reader = KoswatTxtReader()
        _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
        return super(KoswatDikeSelection, _reader.read(txt_file))

    def get_dike_costs(self, reader: KoswatIniReader, ini_file: Path) -> KoswatCosts:
        reader.koswat_ini_fom_type = KoswatCostsIniFom
        return super(KoswatCosts, reader.read(ini_file))

    def build(self) -> KoswatConfiguration:
        _config = KoswatConfiguration()
        _ini_reader = KoswatIniReader()

        # Get FOMs
        _config.general_ini = self.get_general_ini(_ini_reader)
        _config.dike_selection = self.get_dike_selection(
            _config.general_ini.analyse_section.dijksecties_selectie
        )
        _config.scenarios = list(
            self.get_scenarios(
                _ini_reader, _config.general_ini.analyse_section.scenario_invoer
            )
        )
        _config.costs = self.get_dike_costs(
            _ini_reader, _config.general_ini.analyse_section.eenheidsprijzen
        )

        return _config
