from typing import List

from koswat.configuration.converters.koswat_settings_fom_converter_base import (
    KoswatSettingsFomConverterBase,
)
from koswat.configuration.converters.koswat_settings_fom_to_costs_settings import (
    KoswatSettingsFomToCostsSettings,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    AnalysisSectionFom,
    DikeProfileSectionFom,
)
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder


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

    def _get_surroundings_wrapper(self):
        pass

    def convert_settings(self) -> KoswatRunSettings:
        _settings = KoswatRunSettings()

        # Direct mappings.
        _settings.output_dir = self.fom_settings.analyse_section_fom.analysis_output_dir
        _settings.dike_sections = (
            self.fom_settings.analyse_section_fom.dike_selection_txt_fom.dike_sections
        )

        # Define scenarios
        _settings.scenarios = self.fom_settings.analyse_section_fom.scenarios_ini_fom

        # Indirect mappings
        _settings.costs = KoswatSettingsFomToCostsSettings.with_settings_fom(
            self.fom_settings
        ).build()
        _layers_data = self._get_layers_info(self.fom_settings.dike_profile_section_fom)
        _settings.input_profiles = self._get_input_profile_cases(
            self.fom_settings.analyse_section_fom, _layers_data
        )

        # Define surroundings
        _dike_locations = (
            self.fom_settings.analyse_section_fom.dike_section_location_fom
        )
        _surroundings_dirs = list(
            self.fom_settings.surroundings_section.surroundings_database
        )

        return _settings
