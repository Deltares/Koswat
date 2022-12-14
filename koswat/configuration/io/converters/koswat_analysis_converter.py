import logging
from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom_builder import (
    KoswatProfileInputCsvFomBuilder,
)
from koswat.configuration.io.ini.koswat_costs_ini_fom import KoswatCostsIniFom
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsShpReader,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


# TODO: Rename to importers / factory.
def dike_input_profiles_file_to_fom(csv_file: Path) -> List[KoswatInputProfileBase]:
    if not csv_file.is_file():
        logging.error("Dike input profiles csv file not found at {}".format(csv_file))
        return None
    return KoswatCsvReader.with_builder_type(KoswatProfileInputCsvFomBuilder).read(
        csv_file
    )


def dike_sections_location_file_to_fom(shp_file: Path):
    if not shp_file.is_file():
        logging.error("Dike sections shp file not found at {}".format(shp_file))
        return None
    return KoswatDikeLocationsShpReader().read(shp_file)


def dike_selection_file_to_fom(txt_file: Path) -> KoswatDikeSelectionTxtFom:
    if not txt_file.is_file():
        logging.error("Dike selection txt file not found at {}".format(txt_file))
        return None
    _reader = KoswatTxtReader()
    _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
    return _reader.read(txt_file)


def dike_costs_file_to_fom(ini_file: Path) -> KoswatCostsIniFom:
    if not ini_file.is_file():
        logging.error("Dike costs ini file not found at {}".format(ini_file))
        return None
    _reader = KoswatIniReader()
    _reader.koswat_ini_fom_type = KoswatCostsIniFom
    return _reader.read(ini_file)


def scenarios_dir_to_koswat_scenario_list(
    scenario_dir: Path,
) -> List[KoswatSectionScenariosIniFom]:
    if not scenario_dir.is_dir():
        logging.error("Scenarios directory not found at {}".format(scenario_dir))
        return []
    _reader = KoswatIniReader()
    _reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
    _scenarios = []
    for _ini_file in scenario_dir.glob("*.ini"):
        _section_scenarios: KoswatSectionScenariosIniFom = _reader.read(_ini_file)
        _section_scenarios.section_name = _ini_file.stem
        for _s_scenario in _section_scenarios.section_scenarios:
            _scenarios.append(_s_scenario)
    return _scenarios
