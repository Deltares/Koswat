from pathlib import Path
from typing import Iterator, List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
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


def dike_input_profiles_file_to_fom(csv_file: Path) -> List[KoswatInputProfileBase]:
    return KoswatCsvReader.with_builder_type(KoswatProfileInputCsvFomBuilder).read(
        csv_file
    )


def dike_sections_location_file_to_fom(shp_file: Path):
    return KoswatDikeLocationsShpReader().read(shp_file)


def dike_selection_file_to_fom(txt_file: Path) -> KoswatDikeSelectionTxtFom:
    _reader = KoswatTxtReader()
    _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
    return _reader.read(txt_file)


def dike_costs_file_to_fom(ini_file: Path) -> KoswatCostsIniFom:
    _reader = KoswatIniReader()
    _reader.koswat_ini_fom_type = KoswatCostsIniFom
    return _reader.read(ini_file)


def scenarios_dir_to_koswat_scenario_list(
    scenario_dir: Path,
) -> Iterator[KoswatSectionScenariosIniFom]:
    _reader = KoswatIniReader()
    _reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
    for _ini_file in scenario_dir.glob("*.ini"):
        _section_scenarios: KoswatSectionScenariosIniFom = _reader.read(_ini_file)
        _section_scenarios.section_name = _ini_file.stem
        for _s_scenario in _section_scenarios.section_scenarios:
            yield _s_scenario
