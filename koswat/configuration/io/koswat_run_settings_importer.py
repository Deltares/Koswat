import logging
import math
from pathlib import Path
from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.converters.koswat_costs_importer import KoswatCostsImporter
from koswat.configuration.converters.koswat_input_profile_list_importer import (
    KoswatInputProfileListImporter,
)
from koswat.configuration.io.ini import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_costs_ini_fom import KoswatCostsIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import DikeProfileSectionFom
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
    SectionScenarioFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsWrapperShpReader,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
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
            return None

        def profile_is_selected(profile_data: KoswatInputProfileBase) -> bool:
            return profile_data in dike_selection

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

    def _import_selected_dike_section_names(txt_file: Path) -> List[str]:
        if not txt_file.is_file():
            logging.error("Dike selection txt file not found at {}".format(txt_file))
            return None
        _reader = KoswatTxtReader()
        _reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom
        return _reader.read(txt_file).dike_sections

    def _import_dike_costs(ini_file: Path, include_taxes: bool) -> KoswatCostsIniFom:
        if not ini_file.is_file():
            logging.error("Dike costs ini file not found at {}".format(ini_file))
            return None
        _importer = KoswatCostsImporter()
        _importer.ini_configuration = ini_file
        _importer.include_taxes = include_taxes
        return _importer.build()

    def _import_scenario_fom_list(
        scenario_dir: Path, dike_selections: List[str]
    ) -> List[KoswatSectionScenariosIniFom]:
        if not scenario_dir.is_dir():
            logging.error("Scenarios directory not found at {}".format(scenario_dir))
            return []

        def selected_scenario(scenario_file: Path) -> bool:
            if scenario_file.stem not in dike_selections:
                logging.error(
                    "Scenario {} skipped because section was not selected.".format(
                        scenario_file.stem
                    )
                )
                return False
            return True

        def get_scenario(scenario_file: Path) -> KoswatSectionScenariosIniFom:
            _reader = KoswatIniReader()
            _reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom
            _section_scenarios: KoswatSectionScenariosIniFom = _reader.read(
                scenario_file
            )
            _section_scenarios.scenario_section = scenario_file.stem
            return _section_scenarios

        return list(
            map(get_scenario, filter(selected_scenario, scenario_dir.glob("*.ini")))
        )

    def dike_sections_location_file_to_fom(shp_file: Path, dike_selections: List[str]):
        if not shp_file.is_file():
            logging.error("Dike sections shp file not found at {}".format(shp_file))
            return None
        _reader = KoswatDikeLocationsWrapperShpReader()
        _reader.selected_locations = dike_selections
        return _reader.read(shp_file)

    def _get_koswat_scenario(
        self, fom_scenario: SectionScenarioFom, base_profile: KoswatProfileBase
    ) -> KoswatScenario:
        _scenario = KoswatScenario()
        # _scenario.scenario_section = fom_scenario.scenario_section
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
        _dike_costs = self._import_dike_costs()
        _scenario_fom_list = self._import_scenario_fom_list(
            _general_settings.analyse_section_fom.scenarios_ini_file,
            _dike_selected_sections,
        )

        logging.info("Importing INI configuration completed.")

        # Then convert to DOM
        logging.info("Mapping data to Koswat Settings")

        logging.info("Settings import completed.")

        return _run_settings

        # Define scenarios
        # TODO: Reduce complexity.
        # for _fom_scenario in self.fom_settings.analyse_section_fom.scenarios_ini_file:
        #     if _fom_scenario.scenario_section not in _dike_selected_sections:
        #         logging.error(
        #             "Scenario {} won't be run because section was not selected.".format(
        #                 _fom_scenario.scenario_section
        #             )
        #         )
        #         continue
        #     _scenario_output = _run_settings.output_dir / (
        #         "scenario_" + _fom_scenario.scenario_section
        #     )
        #     for (
        #         _shp_dike_fom
        #     ) in self.fom_settings.analyse_section_fom.dike_section_location_file.get_by_section(
        #         _fom_scenario.scenario_section
        #     ):
        #         _csv_db = self.fom_settings.surroundings_section.surroundings_database.get_wrapper_by_traject(
        #             _shp_dike_fom.record.Traject.replace(
        #                 "-", "_"
        #             )  # We know the csv files are with '-' whilst the shp values are '_'
        #         )
        #         if not _csv_db:
        #             logging.warning(
        #                 "No surroundings found for {}".format(
        #                     _shp_dike_fom.record.Traject
        #                 )
        #             )
        #             # TODO: For now we will skip until clarity on what to do in this case.
        #             continue
        #         _surroundings = self._get_surroundings_wrapper(_shp_dike_fom, _csv_db)
        #         for _sub_scenario in _fom_scenario.section_scenarios:
        #             _sub_output = _scenario_output / _sub_scenario.scenario_name
        #             for _input_profile in _input_profile_cases:
        #                 _run_scenario = KoswatRunScenarioSettings()
        #                 _run_scenario.input_profile_case = _input_profile
        #                 _run_scenario.scenario = self._get_koswat_scenario(
        #                     _sub_scenario, _input_profile
        #                 )
        #                 _run_scenario.surroundings = _surroundings
        #                 _run_scenario.costs = _costs
        #                 _run_scenario.output_dir = (
        #                     _sub_output / _input_profile.input_data.dike_section
        #                 )
        #                 _run_settings.run_scenarios.append(_run_scenario)
