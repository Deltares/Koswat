from __future__ import annotations

import abc
import logging

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.ini.koswat_general_ini_fom import KoswatGeneralIniFom
from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings


class KoswatSettingsFomConverterBase(BuilderProtocol, abc.ABC):
    fom_settings: KoswatGeneralIniFom

    def build(self) -> KoswatCostsSettings:
        if not isinstance(self.fom_settings, KoswatGeneralIniFom):
            logging.error("Ini settings required for conversion.")

        return self.convert_settings()

    @abc.abstractmethod
    def convert_settings(self) -> KoswatConfigProtocol:
        raise NotImplementedError("Should be implemented in concrete class.")

    @classmethod
    def with_settings_fom(
        cls, fom_settings: KoswatGeneralIniFom
    ) -> KoswatSettingsFomConverterBase:
        _builder = cls()
        _builder.fom_settings = fom_settings
        return _builder
