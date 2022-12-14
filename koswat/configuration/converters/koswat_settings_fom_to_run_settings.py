from koswat.configuration.converters.koswat_settings_fom_converter_base import (
    KoswatSettingsFomConverterBase,
)
from koswat.configuration.converters.koswat_settings_ini_fom_to_costs_settings import (
    KoswatSettingsIniFomToCostsSettings,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import KoswatSettingsIniFom
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings


class KoswatSettingsFomToRunSettings(KoswatSettingsFomConverterBase):
    def convert_settings(self) -> KoswatRunSettings:
        _settings = KoswatRunSettings()
        _settings.costs = KoswatSettingsIniFomToCostsSettings.with_settings_fom(
            self.fom_settings
        ).build()
        return _settings
