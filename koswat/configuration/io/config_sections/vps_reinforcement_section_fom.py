import math
from configparser import SectionProxy
from typing import Any

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class VPSReinforcementSectionFom(ConfigSectionFomBase):
    active: bool
    polderside_berm_width_vps: float
    soil_surtax_factor: SurtaxFactorEnum
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _bool_mappings = dict(
        actief="active",
    )
    _float_mappings = dict(
        binnen_berm_breedte_vps="polderside_berm_width_vps",
    )
    _surtax_mappings = dict(
        opslag_factor_grond="soil_surtax_factor",
        opslagfactor_constructief="constructive_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )

    @classmethod
    def from_ini(cls, ini_config: SectionProxy) -> "VPSReinforcementSectionFom":
        _section = cls()
        _section._set_bool_values(dict(ini_config), cls._bool_mappings, False)
        _section._set_float_values(dict(ini_config), cls._float_mappings, math.nan)
        _section._set_surtax_factor_values(
            dict(ini_config), cls._surtax_mappings, SurtaxFactorEnum.NORMAAL
        )
        return _section

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> "VPSReinforcementSectionFom":
        _section = cls()
        _section._set_bool_values(input_dict, cls._bool_mappings, None)
        _section._set_float_values(input_dict, cls._float_mappings, None)
        _section._set_surtax_factor_values(input_dict, cls._surtax_mappings, None)
        return _section
