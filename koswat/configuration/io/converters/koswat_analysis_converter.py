from pathlib import Path
from typing import Iterator, List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.configuration.io.csv.koswat_input_profiles_csv_fom_builder import (
    KoswatProfileInputCsvFomBuilder,
)
from koswat.configuration.io.ini import KoswatCostsIniFom, KoswatSectionScenariosIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import AnalysisSectionFom
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.models import KoswatCosts, KoswatDikeSelection, KoswatScenario
from koswat.configuration.models.koswat_general_settings import AnalysisSettings
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


def _dike_input_profiles_file_to_dom(csv_file: Path) -> List[KoswatInputProfileBase]:
    _input_profile_fom: KoswatInputProfilesCsvFom = KoswatCsvReader.with_builder_type(
        KoswatProfileInputCsvFomBuilder
    ).read(csv_file)
    _dom_list = []
    for _csv_fom in _input_profile_fom.input_profile_fom_list:
        _input_profile = KoswatInputProfileBase()
        _input_profile.dike_section = _csv_fom.get("dikesection", "")
        _input_profile.buiten_maaiveld = _csv_fom["buiten_maaiveld"]
        _input_profile.buiten_talud = _csv_fom["buiten_talud"]
        _input_profile.buiten_berm_hoogte = _csv_fom["buiten_berm_hoogte"]
        _input_profile.buiten_berm_breedte = _csv_fom["buiten_berm_lengte"]  #
        _input_profile.kruin_hoogte = _csv_fom["kruin_hoogte"]
        _input_profile.kruin_breedte = _csv_fom["kruin_breedte"]
        _input_profile.binnen_talud = _csv_fom["binnen_talud"]
        _input_profile.binnen_berm_hoogte = _csv_fom["binnen_berm_hoogte"]
        _input_profile.binnen_berm_breedte = _csv_fom["binnen_berm_lengte"]  #
        _input_profile.binnen_maaiveld = _csv_fom["binnen_maaiveld"]
        _dom_list.append(_input_profile)
    return _dom_list


def _scenarios_path_to_koswat_scenario_list(
    reader: KoswatIniReader, scenario_dir: Path
) -> Iterator[KoswatScenario]:
    reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
    for _ini_file in scenario_dir.glob("*.ini"):
        _section_scenarios: KoswatSectionScenariosIniFom = reader.read(_ini_file)
        _section_scenarios.section_name = _ini_file.stem
        for _s_scenario in _section_scenarios.section_scenarios:
            yield _s_scenario


def _dike_selection_file_to_dom(txt_file: Path) -> KoswatDikeSelection:
    _reader = KoswatTxtReader()
    _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
    return _reader.read(txt_file)


def _dike_costs_file_to_dom(reader: KoswatIniReader, ini_file: Path) -> KoswatCosts:
    reader.koswat_ini_fom_type = KoswatCostsIniFom
    return reader.read(ini_file)


def analysis_settings_fom_to_dom(analysis_fom: AnalysisSectionFom) -> AnalysisSettings:
    """
    Converts an analysis `AnalysisSectionFom` into a section, parsing its values into corresponding `DataObjectModel`s when possible.

    Args:
        analysis_fom (AnalysisSectionFom): Instance `FileObjectModel` to convert into a `DataObjectModel`.

    Returns:
        AnalysisSettings: Instance of a `DataObjectModel`.
    """
    _ini_reader = KoswatIniReader()
    _settings = AnalysisSettings()
    _settings.dike_selection = _dike_selection_file_to_dom(
        analysis_fom.dike_sections_selection_ini_file
    )
    _settings.scenarios = list(
        _scenarios_path_to_koswat_scenario_list(_ini_reader, analysis_fom.scenarios_dir)
    )
    _settings.costs = _dike_costs_file_to_dom(_ini_reader, analysis_fom.costs_ini_file)
    _settings.analysis_output = analysis_fom.analysis_output_dir
    _settings.dijksectie_ligging = analysis_fom.dijksectie_ligging
    _settings.dike_sections_input_profile = _dike_input_profiles_file_to_dom(
        analysis_fom.dike_sections_input_profiles_csv_file
    )
    _settings.include_taxes = analysis_fom.include_taxes
    return _settings
