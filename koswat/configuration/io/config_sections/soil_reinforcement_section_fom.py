import math
from configparser import SectionProxy
from typing import Any

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class SoilReinforcementSectionFom(ConfigSectionFomBase):
    min_berm_height: float
    max_berm_height_factor: float
    factor_increase_berm_height: float
    soil_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _float_mappings = dict(
        min_bermhoogte="min_berm_height",
        max_bermhoogte_factor="max_berm_height_factor",
        factor_toename_bermhoogte="factor_increase_berm_height",
    )
    _surtax_mappings = dict(
        opslagfactor_grond="soil_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )

    @classmethod
    def from_ini(cls, ini_config: SectionProxy) -> "SoilReinforcementSectionFom":
        _section = cls()
        _section._set_float_values(dict(ini_config), cls._float_mappings, math.nan)
        _section._set_surtax_factor_values(
            dict(ini_config), cls._surtax_mappings, SurtaxFactorEnum.NORMAAL
        )
        return _section

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> "SoilReinforcementSectionFom":
        _section = cls()
        _section._set_float_values(input_dict, cls._float_mappings, None)
        _section._set_surtax_factor_values(input_dict, cls._surtax_mappings, None)
        return _section
