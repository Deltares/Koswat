import logging
import math
from pathlib import Path

from koswat.configuration.io.ini import KoswatGeneralIniFom
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    DikeProfileSectionFom,
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
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
from koswat.configuration.io.surroundings_wrapper_collection_importer import (
    SurroundingsWrapperCollectionImporter,
)
from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.configuration.settings.koswat_run_settings import (
    KoswatRunScenarioSettings,
    KoswatRunSettings,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.core.io.txt.koswat_txt_reader import KoswatTxtReader
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class KoswatRunSettingsImporter(KoswatImporterProtocol):
    def import_from(self, from_path: Path) -> KoswatRunSettings:
        # First get the FOM
        logging.info("Importing INI configuration from {}".format(from_path))
        _general_settings = self._import_general_settings(from_path)
        _output_dir = _general_settings.analysis_section.analysis_output_dir
        _dike_selected_sections = self._import_selected_dike_section_names(
            _general_settings.analysis_section.dike_selection_txt_file
        )
        _input_profile_cases = self._import_dike_input_profiles_list(
            csv_file=_general_settings.analysis_section.input_profiles_csv_file,
            dike_selection=_dike_selected_sections,
            layers_info=self._get_layers_info(_general_settings.dike_profile_section),
        )
        _dike_costs = self._import_dike_costs(
            ini_file=_general_settings.analysis_section.costs_ini_file,
            include_taxes=_general_settings.analysis_section.include_taxes,
        )
        _scenario_fom_list = self._import_scenario_fom_list(
            _general_settings.analysis_section.scenarios_ini_file,
            _dike_selected_sections,
        )
        _surroundings_fom = self._import_surroundings_wrapper(
            _general_settings.surroundings_section,
            _general_settings.infrastructuur_section,
            _general_settings.analysis_section.dike_section_location_shp_file,
            [_s.scenario_dike_section for _s in _scenario_fom_list],
        )
        _reinforcement_settings = self._get_reinforcement_settings(_general_settings)

        logging.info("Importing INI configuration completed.")

        # Then convert to DOM
        logging.info("Mapping data to Koswat Settings")
        _run_settings = self._get_run_settings(
            _reinforcement_settings,
            _input_profile_cases,
            _scenario_fom_list,
            _dike_costs,
            _surroundings_fom,
            _output_dir,
        )
        logging.info("Settings import completed.")

        return _run_settings

    def _get_run_settings(
        self,
        reinforcement_settings: KoswatReinforcementSettings,
        input_profiles: list[KoswatProfileBase],
        fom_scenario_list: list[KoswatSectionScenariosIniFom],
        costs_settings: KoswatCostsSettings,
        surroundings_fom: list[SurroundingsWrapper],
        output_dir: Path,
    ) -> KoswatRunSettings:
        _run_settings = KoswatRunSettings()
        _run_settings.output_dir = output_dir
        for _ip in input_profiles:
            # Find this input profile scenarios.
            _fom_scenario = next(
                (
                    _fs
                    for _fs in fom_scenario_list
                    if _fs.scenario_dike_section == _ip.input_data.dike_section
                ),
                None,
            )
            if not _fom_scenario:
                logging.warning(
                    "No scenario found for selected section {}.".format(
                        _ip.input_data.dike_section
                    )
                )
                continue

            # Define section-dependent properties
            _surrounding = next(
                (
                    _surrounding
                    for _surrounding in surroundings_fom
                    if _surrounding.dike_section == _fom_scenario.scenario_dike_section
                ),
                None,
            )
            _dike_output_dir = output_dir / ("dike_" + _ip.input_data.dike_section)

            # Create new run scenario setting
            logging.info(
                "Creating scenarios for profile {}.".format(_ip.input_data.dike_section)
            )
            for _sub_scenario in _fom_scenario.section_scenarios:
                _run_scenario = KoswatRunScenarioSettings()
                _run_scenario.input_profile_case = _ip
                _run_scenario.scenario = self._get_koswat_scenario(_sub_scenario, _ip)
                _run_scenario.reinforcement_settings = reinforcement_settings
                _run_scenario.surroundings = _surrounding
                _run_scenario.costs_setting = costs_settings
                _run_scenario.output_dir = _dike_output_dir / (
                    "scenario_" + _sub_scenario.scenario_name.lower()
                )
                logging.info(
                    "Created sub scenario {}.".format(_sub_scenario.scenario_name)
                )
                _run_settings.run_scenarios.append(_run_scenario)
        logging.info(
            "Finished generating koswat scenarios. A total of {} scenarios were created.".format(
                len(_run_settings.run_scenarios)
            )
        )
        return _run_settings

    def _import_general_settings(self, ini_config_file: Path) -> KoswatGeneralIniFom:
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatGeneralIniFom
        return reader.read(ini_config_file)

    def _get_reinforcement_settings(
        self, general_settings: KoswatGeneralIniFom
    ) -> KoswatReinforcementSettings:
        _reinforcement_settings = KoswatReinforcementSettings(
            soil_settings=KoswatSoilSettings(
                **(general_settings.soil_measure_section.__dict__)
            ),
            vps_settings=KoswatVPSSettings(**(general_settings.vps_section.__dict__)),
            piping_wall_settings=KoswatPipingWallSettings(
                **(general_settings.piping_wall_section.__dict__)
            ),
            stability_wall_settings=KoswatStabilityWallSettings(
                **(general_settings.stability_wall_section.__dict__)
            ),
            cofferdam_settings=KoswatCofferdamSettings(
                **(general_settings.cofferdam_section.__dict__)
            ),
        )
        return _reinforcement_settings

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
        self, csv_file: Path, dike_selection: list[str], layers_info: dict
    ) -> list[KoswatInputProfileBase]:
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

        _profile_list = list(
            map(
                to_koswat_profile,
                filter(
                    profile_is_selected,
                    KoswatInputProfileListImporter().import_from(csv_file),
                ),
            )
        )
        return _profile_list

    def _import_selected_dike_section_names(self, txt_file: Path) -> list[str]:
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
        _importer.include_taxes = include_taxes
        return _importer.import_from(ini_file)

    def _import_scenario_fom_list(
        self, scenario_dir: Path, dike_selections: list[str]
    ) -> list[KoswatSectionScenariosIniFom]:
        _reader = KoswatSectionScenarioListIniDirReader()
        _reader.dike_selection = dike_selections
        return _reader.read(scenario_dir)

    def _import_surroundings_wrapper(
        self,
        surroundings_section: SurroundingsSectionFom,
        infrastructure_section: InfrastructureSectionFom,
        traject_shp_file: Path,
        dike_selections: list[str],
    ) -> list[SurroundingsWrapper]:
        _builder = SurroundingsWrapperCollectionImporter(
            infrastructure_section_fom=infrastructure_section,
            traject_loc_shp_file=traject_shp_file,
            selected_locations=dike_selections,
            surroundings_section_fom=surroundings_section,
        )
        return _builder.build()

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

        _scenario.crest_width = get_valid_value("crest_width")
        _scenario.waterside_slope = get_valid_value("waterside_slope")
        return _scenario
