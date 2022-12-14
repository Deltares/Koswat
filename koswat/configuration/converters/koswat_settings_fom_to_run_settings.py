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
    KoswatSettingsIniFom,
)
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings
from koswat.dike.material.koswat_material_type import KoswatMaterialType
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

    def _get_input_profile_cases(
        self, section_fom: AnalysisSectionFom, layers_info: dict
    ) -> List[KoswatProfileBase]:
        _cases = []
        for _input_case in section_fom.input_profiles_csv_fom:
            _input_profile = KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=_input_case,
                    layers_data=layers_info,
                    profile_type=KoswatProfileBase,
                )
            )
            _cases.append(_input_profile)
        return _cases

    def convert_settings(self) -> KoswatRunSettings:
        _settings = KoswatRunSettings()
        _settings.costs = KoswatSettingsFomToCostsSettings.with_settings_fom(
            self.fom_settings
        ).build()
        _layers_data = self._get_layers_info(self.fom_settings.dike_profile_section_fom)
        _settings.input_profiles = self._get_input_profile_cases(
            self.fom_settings.analyse_section_fom, _layers_data
        )

        # Define scenarios
        _settings.scenarios = self.fom_settings.analysis_settings.scenarios

        # Define surroundings
        _settings.surroundings = list(
            self.fom_settings.surroundings_settings.surroundings_database.iterdir()
        )

        return _settings
