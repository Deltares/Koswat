import logging
from typing import List

from koswat.configuration.converters.koswat_settings_fom_converter_base import (
    KoswatSettingsFomConverterBase,
)
from koswat.configuration.converters.koswat_settings_fom_to_costs_settings import (
    KoswatSettingsFomToCostsSettings,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCollectionCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    AnalysisSectionFom,
    DikeProfileSectionFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
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
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


class KoswatSettingsFomToRunSettings(KoswatSettingsFomConverterBase):
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

    def _get_koswat_input_profile_base(self, fom_dict: dict) -> KoswatInputProfileBase:
        _input_profile = KoswatInputProfileBase()
        _input_profile.dike_section = fom_dict["dijksectie"]
        _input_profile.buiten_maaiveld = float(fom_dict["buiten_maaiveld"])
        _input_profile.buiten_talud = float(fom_dict["buiten_talud"])
        _input_profile.buiten_berm_hoogte = float(fom_dict["buiten_berm_hoogte"])
        _input_profile.buiten_berm_breedte = float(fom_dict["buiten_berm_lengte"])
        _input_profile.kruin_hoogte = float(fom_dict["kruin_hoogte"])
        _input_profile.kruin_breedte = float(fom_dict["kruin_breedte"])
        _input_profile.binnen_talud = float(fom_dict["binnen_talud"])
        _input_profile.binnen_berm_hoogte = float(fom_dict["binnen_berm_hoogte"])
        _input_profile.binnen_berm_breedte = float(fom_dict["binnen_berm_lengte"])
        _input_profile.binnen_maaiveld = float(fom_dict["binnen_maaiveld"])
        return _input_profile

    def _get_input_profile_cases(
        self, section_fom: AnalysisSectionFom, layers_info: dict
    ) -> List[KoswatProfileBase]:
        _cases = []
        for _input_case in section_fom.input_profiles_csv_fom.input_profile_fom_list:
            if (
                not _input_case["dijksectie"]
                in section_fom.dike_selection_txt_fom.dike_sections
            ):
                continue
            _input_profile = KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=self._get_koswat_input_profile_base(_input_case),
                    layers_data=layers_info,
                    profile_type=KoswatProfileBase,
                )
            ).build()
            _cases.append(_input_profile)
        return _cases

    def _get_surroundings_wrapper(
        self,
        trajects_fom: KoswatDikeLocationsShpFom,
        surroundings_fom: KoswatTrajectSurroundingsWrapperCsvFom,
    ) -> SurroundingsWrapper:
        _builder = SurroundingsWrapperBuilder()
        _builder.surroundings_fom = surroundings_fom
        _builder.trajects_fom = trajects_fom
        return _builder.build()

    def convert_settings(self) -> KoswatRunSettings:
        _run_settings = KoswatRunSettings()

        # Direct mappings.
        _output_dir = self.fom_settings.analyse_section_fom.analysis_output_dir
        _dike_selected_sections = (
            self.fom_settings.analyse_section_fom.dike_selection_txt_fom.dike_sections
        )
        _costs = KoswatSettingsFomToCostsSettings.with_settings_fom(
            self.fom_settings
        ).build()

        # Input profiles
        _run_settings.input_profile_cases = self._get_input_profile_cases(
            self.fom_settings.analyse_section_fom,
            self._get_layers_info(self.fom_settings.dike_profile_section_fom),
        )

        # Define scenarios
        for _fom_scenario in self.fom_settings.analyse_section_fom.scenarios_ini_fom:
            if _fom_scenario.scenario_section not in _dike_selected_sections:
                logging.error(
                    "Scenario {} won't be run because section was not selected.".format(
                        _fom_scenario.scenario_section
                    )
                )
                continue
            _scenario_output = _output_dir / _fom_scenario.scenario_section
            for (
                _shp_dike_fom
            ) in self.fom_settings.analyse_section_fom.dike_section_location_fom.get_by_section(
                _fom_scenario.scenario_section
            ):
                _csv_db = self.fom_settings.surroundings_section.surroundings_database.get_wrapper_by_traject(
                    _shp_dike_fom.record.Traject.replace(
                        "-", "_"
                    )  # We know the csv files are with '-' whilst the shp values are '_'
                )
                if not _csv_db:
                    logging.warning(
                        "No surroundings found for {}".format(
                            _shp_dike_fom.record.Traject
                        )
                    )
                    # TODO: For now we will skip until clarity on what to do in this case.
                    continue
                _surroundings = self._get_surroundings_wrapper(_shp_dike_fom, _csv_db)
                for _sub_scenario in _fom_scenario.section_scenarios:
                    _run_scenario = KoswatRunScenarioSettings()
                    _run_scenario.scenario = KoswatScenario()
                    _run_scenario.scenario.__dict__ = _sub_scenario.__dict__
                    _run_scenario.scenario.scenario_section = (
                        _fom_scenario.scenario_section
                    )
                    _run_scenario.surroundings = _surroundings
                    _run_scenario.costs = _costs
                    _run_scenario.output_dir = (
                        _scenario_output / _sub_scenario.scenario_name
                    )
                    _run_settings.run_scenarios.append(_run_scenario)

        return _run_settings
