from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class SoilReinforcementSectionFom(ConfigSectionFomBase):
    active: bool
    min_berm_height: float
    max_berm_height_factor: float
    factor_increase_berm_height: float
    soil_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _bool_mappings = dict(
        actief="active",
    )
    _float_mappings = dict(
        min_bermhoogte="min_berm_height",
        max_bermhoogte_factor="max_berm_height_factor",
        factor_toename_bermhoogte="factor_increase_berm_height",
    )
    _surtax_mappings = dict(
        opslagfactor_grond="soil_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )
