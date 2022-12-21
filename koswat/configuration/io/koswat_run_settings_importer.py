import logging
import math
from pathlib import Path
from typing import Any, List

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import DikeProfileSectionFom
from koswat.configuration.io.ini.koswat_scenario_list_ini_dir_reader import (
    KoswatSectionScenarioListIniDirReader,
)
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
    SectionScenarioFom,
)
from koswat.configuration.io.koswat_costs_importer import KoswatCostsImporter
from koswat.configuration.io.koswat_input_profile_list_importer import (
    KoswatInputProfileListImporter,
)
from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsImporter,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.configuration.settings.koswat_run_settings import (
    KoswatRunScenarioSettings,
    KoswatRunSettings,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


class KoswatRunSettingsImporter(BuilderProtocol):
    ini_configuration: Path

    def __init__(self) -> None:
        self.ini_configuration = None

    def _import_general_settings(self) -> KoswatGeneralIniFom:
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(self.ini_configuration)

    def _get_layers_info(self, section_fom: DikeProfileSectionFom) -> dict:
        return dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(
                    material=KoswatMaterialType.GRASS,
                    depth=section_fom.thickness_grass_layer,
                ),
                dict(
                    material=KoswatMaterialType.CLAY,
                    depth=section_fom.thickness_clay_layer,
                ),
            ],
        )

    def _import_dike_input_profiles_list(
        self, csv_file: Path, dike_selection: List[str], layers_info: dict
    ) -> List[KoswatInputProfileBase]:
        if not csv_file.is_file():
            logging.error(
                "Dike input profiles csv file not found at {}".format(csv_file)
            )
            return []

        def profile_is_selected(profile_data: KoswatInputProfileBase) -> bool:
            return profile_data.dike_section in dike_selection

        def to_koswat_profile(
            profile_data: KoswatInputProfileBase,
        ) -> KoswatProfileBase:
            return KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=profile_data,
                    layers_data=layers_info,
                    profile_type=KoswatProfileBase,
                )
            ).build()

        _input_profile_importer = KoswatInputProfileListImporter()
        _input_profile_importer.ini_configuration = csv_file
        _profile_list = list(
            map(
                to_koswat_profile,
                filter(profile_is_selected, _input_profile_importer.build()),
            )
        )
        return _profile_list

    def _import_selected_dike_section_names(self, txt_file: Path) -> List[str]:
        if not txt_file.is_file():
            logging.error("Dike selection txt file not found at {}".format(txt_file))
            return []
        _reader = KoswatTxtReader()
        _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
        return _reader.read(txt_file).dike_sections

    def _import_dike_costs(
        self, ini_file: Path, include_taxes: bool
    ) -> KoswatCostsSettings:
        if not ini_file.is_file():
            logging.error("Dike costs ini file not found at {}".format(ini_file))
            return None
        _importer = KoswatCostsImporter()
        _importer.ini_configuration = ini_file
        _importer.include_taxes = include_taxes
        return _importer.build()

    def _import_scenario_fom_list(
        self, scenario_dir: Path, dike_selections: List[str]
    ) -> List[KoswatSectionScenariosIniFom]:
        _reader = KoswatSectionScenarioListIniDirReader()
        _reader.dike_selection = dike_selections
        return _reader.read(scenario_dir)

    def _import_surroundings(
        self, surroundings_dir: Path, traject_shp_file: Path, dike_selections: List[str]
    ) -> Any:
        _importer = KoswatSurroundingsImporter()
        _importer.surroundings_csv_dir = surroundings_dir
        _importer.traject_loc_shp_file = traject_shp_file
        _importer.selected_locations = dike_selections
        return _importer.build()

    def _get_koswat_scenario(
        self, fom_scenario: SectionScenarioFom, base_profile: KoswatProfileBase
    ) -> KoswatScenario:
        _scenario = KoswatScenario()
        _scenario.scenario_name = fom_scenario.scenario_name
        _scenario.d_h = fom_scenario.d_h
        _scenario.d_s = fom_scenario.d_s
        _scenario.d_p = fom_scenario.d_p

        def get_valid_value(prop_name: str) -> float:
            _value = getattr(fom_scenario, prop_name)
            if not _value or math.isnan(_value):
                return getattr(base_profile.input_data, prop_name)
            return _value

        _scenario.kruin_breedte = get_valid_value("kruin_breedte")
        _scenario.buiten_talud = get_valid_value("buiten_talud")
        return _scenario

    def build(self) -> KoswatRunSettings:
        _run_settings = KoswatRunSettings()

        # First get the FOM
        logging.info(
            "Importing INI configuration from {}".format(self.ini_configuration)
        )
        _general_settings = self._import_general_settings()
        _run_settings.output_dir = (
            _general_settings.analyse_section_fom.analysis_output_dir
        )
        _dike_selected_sections = self._import_selected_dike_section_names(
            _general_settings.analyse_section_fom.dike_selection_txt_file
        )
        _run_settings.input_profile_cases = self._import_dike_input_profiles_list(
            csv_file=_general_settings.analyse_section_fom.input_profiles_csv_file,
            dike_selection=_dike_selected_sections,
            layers_info=self._get_layers_info(
                _general_settings.dike_profile_section_fom
            ),
        )
        _dike_costs = self._import_dike_costs(
            ini_file=_general_settings.analyse_section_fom.costs_ini_file,
            include_taxes=_general_settings.analyse_section_fom.include_taxes,
        )
        _scenario_fom_list = self._import_scenario_fom_list(
            _general_settings.analyse_section_fom.scenarios_ini_file,
            _dike_selected_sections,
        )

        _surroundings_fom = self._import_surroundings(
            _general_settings.surroundings_section.surroundings_database_dir,
            _general_settings.analyse_section_fom.dike_section_location_shp_file,
            [_s.scenario_section for _s in _scenario_fom_list],
        )

        logging.info("Importing INI configuration completed.")

        # Then convert to DOM
        logging.info("Mapping data to Koswat Settings")
        self.get_scenarios(
            _run_settings, _scenario_fom_list, _dike_costs, _surroundings_fom
        )
        logging.info("Settings import completed.")

        return _run_settings

    def get_scenarios(
        self,
        run_settings: KoswatRunSettings,
        fom_scenario: List[KoswatSectionScenariosIniFom],
        costs_settings: KoswatCostsSettings,
        surroundings_fom: List[SurroundingsWrapper],
    ) -> None:
        for _fom_scenario in fom_scenario:
            _scenario_output = run_settings.output_dir / (
                "scenario_" + _fom_scenario.scenario_section
            )
            _surrounding = next(
                filter(
                    lambda x: x.dike_section == _fom_scenario.scenario_section,
                    surroundings_fom,
                ),
                None,
            )
            for _sub_scenario in _fom_scenario.section_scenarios:
                _sub_output = _scenario_output / _sub_scenario.scenario_name
                for _input_profile in run_settings.input_profile_cases:
                    _run_scenario = KoswatRunScenarioSettings()
                    _run_scenario.input_profile_case = _input_profile
                    _run_scenario.scenario = self._get_koswat_scenario(
                        _sub_scenario, _input_profile
                    )
                    _run_scenario.surroundings = _surrounding
                    _run_scenario.costs = costs_settings
                    _run_scenario.output_dir = (
                        _sub_output / _input_profile.input_data.dike_section
                    )
                    run_settings.run_scenarios.append(_run_scenario)
